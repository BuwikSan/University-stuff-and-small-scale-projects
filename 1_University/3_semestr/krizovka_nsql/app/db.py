"""
Database layer - MongoDB + Redis
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import logging

from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import redis

from .models import CrisisEvent

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Správce databází - MongoDB (persistent) + Redis (cache)"""
    
    def __init__(self, mongo_uri: str, redis_url: str, db_name: str):
        self.mongo_uri = mongo_uri
        self.redis_url = redis_url
        self.db_name = db_name
        
        # Lazy load - připojit až když je potřeba
        self._mongo_client: Optional[MongoClient] = None
        self._redis_client: Optional[redis.Redis] = None
        self._db = None
    
    @property
    def mongo(self) -> MongoClient:
        """Lazy-load MongoDB connection"""
        if self._mongo_client is None:
            try:
                self._mongo_client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
                # Test connection
                self._mongo_client.server_info()
                self._db = self._mongo_client[self.db_name]
                logger.info(f"✓ Připojen k MongoDB: {self.db_name}")
            except (ConnectionFailure, ServerSelectionTimeoutError) as e:
                logger.error(f"✗ MongoDB spojení selhalo: {e}")
                self._mongo_client = None
                raise
        return self._mongo_client
    
    @property
    def redis(self) -> redis.Redis:
        """Lazy-load Redis connection"""
        if self._redis_client is None:
            try:
                self._redis_client = redis.from_url(self.redis_url, decode_responses=True)
                # Test connection
                self._redis_client.ping()
                logger.info("✓ Připojen k Redis")
            except Exception as e:
                logger.error(f"✗ Redis spojení selhalo: {e}")
                self._redis_client = None
                raise
        return self._redis_client
    
    @property
    def db(self):
        """Přístup k MongoDB databázi"""
        if self._db is None:
            _ = self.mongo  # Trigger lazy load
        return self._db
    
    def get_collection(self, name: str):
        """Vrať MongoDB kolekci"""
        return self.db[name]
    
    # ==================== CRISIS EVENTS ====================
    
    def clear_all_events(self) -> int:
        """Smaž VŠECHNY eventy z databáze. Vrátí počet smazaných."""
        try:
            collection = self.get_collection("events")
            result = collection.delete_many({})
            
            # Invaliduj všechny cache
            self._invalidate_events_cache()
            self.redis.delete("events:today")
            
            logger.info(f"✓ Smazáno {result.deleted_count} eventů z databáze")
            return result.deleted_count
        except Exception as e:
            logger.error(f"✗ Chyba při mazání eventů: {e}")
            raise
    
    def create_event(self, event: CrisisEvent) -> str:
        """
        Vytvoř novou crisis event.
        Vrátí event ID.
        """
        try:
            collection = self.get_collection("events")
            event_dict = event.to_dict()
            result = collection.insert_one(event_dict)
            
            # Invaliduj cache
            self._invalidate_events_cache()
            
            logger.info(f"✓ Event vytořen: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"✗ Chyba při vytváření eventu: {e}")
            raise
    
    def get_event(self, event_id: str) -> Optional[CrisisEvent]:
        """Vrať event podle ID"""
        try:
            from bson.objectid import ObjectId
            collection = self.get_collection("events")
            event_dict = collection.find_one({"_id": ObjectId(event_id)})
            if event_dict:
                return CrisisEvent.from_dict(event_dict)
            return None
        except Exception as e:
            logger.error(f"✗ Chyba při načítání eventu: {e}")
            return None
    
    def get_all_events(self, limit: int = 50, skip: int = 0) -> List[CrisisEvent]:
        """
        Vrať všechny eventy seřazené podle času (nejnovější první).
        Cache se používá pro všechny dotazy s limit <= 50.
        """
        # Zkus cache pro rozumné limity
        cache_key = "events:all"
        if limit <= 50:
            try:
                cached = self.redis.get(cache_key)
                if cached:
                    data = json.loads(cached)
                    all_events = [CrisisEvent.from_dict(d) for d in data]
                    # Slicuj v Pythonu podle skip/limit
                    return all_events[skip:skip+limit]
            except Exception as e:
                logger.warning(f"Cache read failed: {e}")
        
        # Pokud cache selže nebo je velký limit, jdi do MongoDB
        try:
            collection = self.get_collection("events")
            events_data = list(
                collection.find()
                .sort("created_at", DESCENDING)
                .limit(limit)
                .skip(skip)
            )
            
            events = [CrisisEvent.from_dict(d) for d in events_data]
            
            # Ulož VŠECHNY eventy do cache (bez limit/skip)
            if limit <= 50 and skip == 0:
                try:
                    all_events_data = list(
                        collection.find()
                        .sort("created_at", DESCENDING)
                    )
                    self.redis.setex(
                        cache_key,
                        300,
                        json.dumps([e.to_dict() for e in [CrisisEvent.from_dict(d) for d in all_events_data]], default=str)
                    )
                except Exception as e:
                    logger.warning(f"Cache write failed: {e}")
            
            return events
        except Exception as e:
            logger.error(f"✗ Chyba při načítání eventů: {e}")
            return []
    
    def count_events(self) -> int:
        """Vrať počet všech eventů"""
        try:
            # Zkus cache
            cache_key = "events:count"
            try:
                cached = self.redis.get(cache_key)
                if cached:
                    return int(cached)
            except:
                pass
            
            collection = self.get_collection("events")
            count = collection.count_documents({})
            
            # Cache na 5 minut
            try:
                self.redis.setex(cache_key, 300, str(count))
            except:
                pass
            
            return count
        except Exception as e:
            logger.error(f"✗ Chyba při počítání eventů: {e}")
            return 0
    
    def count_today_events(self) -> int:
        """Vrať počet eventů hlášených dnes"""
        try:
            from datetime import datetime, timedelta
            
            # Zkus cache
            cache_key = "events:today"
            try:
                cached = self.redis.get(cache_key)
                if cached:
                    return int(cached)
            except:
                pass
            
            # Spočítej kríze od půlnoci dneška
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)
            
            collection = self.get_collection("events")
            count = collection.count_documents({
                "created_at": {
                    "$gte": today_start,
                    "$lt": today_end
                }
            })
            
            # Cache na 5 minut
            try:
                self.redis.setex(cache_key, 300, str(count))
            except:
                pass
            
            return count
        except Exception as e:
            logger.error(f"✗ Chyba při počítání dnešních eventů: {e}")
            return 0
    
    def delete_event(self, event_id: str) -> bool:
        """Smaž event"""
        try:
            from bson.objectid import ObjectId
            collection = self.get_collection("events")
            result = collection.delete_one({"_id": ObjectId(event_id)})
            if result.deleted_count > 0:
                self._invalidate_events_cache()
                logger.info(f"✓ Event smazán: {event_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"✗ Chyba při smazání eventu: {e}")
            return False
    
    def _invalidate_events_cache(self):
        """Vynuluj relevantní cache klíče"""
        try:
            self.redis.delete("events:all", "events:count")
        except Exception as e:
            logger.warning(f"Cache invalidation failed: {e}")
    
    # ==================== HEALTH CHECK ====================
    
    def health_check(self) -> Dict[str, bool]:
        """Ověř připojení ke všem databázím"""
        result = {"mongo": False, "redis": False}
        
        try:
            self.mongo.server_info()
            result["mongo"] = True
        except:
            pass
        
        try:
            self.redis.ping()
            result["redis"] = True
        except:
            pass
        
        return result
