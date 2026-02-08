"""
Naplnění databáze testovacími daty - 20 realistických krizí
Spuštění: python -c "from app.initial_db_fill import fill_db; fill_db()"
"""

from datetime import datetime, timedelta
from .models import CrisisEvent, CRISIS_TYPES
from .db import DatabaseManager
import random
import os

# Česká města a lokace
CZECH_LOCATIONS = [
    ("Praha, Staroměstské náměstí", 50.0755, 14.4378),
    ("Brno, Svobody", 49.1953, 16.6141),
    ("Ostrava, nádraží", 49.8175, 18.2844),
    ("Plzeň, Náměstí Republiky", 49.7384, 13.3772),
    ("Liberec, České Švýcarsko", 50.7671, 14.0573),
    ("Olomouc, Horní náměstí", 49.5952, 17.2519),
    ("České Budějovice, Přemysla Otakara II", 48.9745, 14.4729),
    ("Hradec Králové, Gočárův most", 50.2087, 15.8326),
    ("Pardubice, Masarykovo nábř.", 50.0393, 15.7721),
    ("Zhořelec, D7 směr Mladá Boleslav", 50.5667, 13.5),
    ("Kladno, nemocnice", 50.1427, 14.0936),
    ("Ústí nad Labem, přístav", 50.6628, 14.0335),
    ("Tábor, Husův pomník", 49.4111, 14.6613),
    ("Cheb, Špalíček", 50.0793, 12.3697),
    ("Modelová, průmyslová zóna", 50.2000, 14.5000),
]

# Příklady krizí
CRISIS_TEMPLATES = [
    {
        "title": "Povodně v Praze",
        "description": "Řeka Vltava vyšla z břehů kvůli dlouhodobým srážkám. Evakuace 300 lidí, zátopený průmyslový park.",
        "type": "přírodní_katastrofa",
        "severity_range": (3, 5),
        "locations": [0],
    },
    {
        "title": "Havárie na D1 u Brna",
        "description": "Srazilo se 8 vozů, tři mrtvých na místě. Vozidlo narazilo do kamionu s živočichy.",
        "type": "dopravní_nehoda",
        "severity_range": (4, 5),
        "locations": [1],
    },
    {
        "title": "Požár v bytovém domě v Ostravě",
        "description": "Oheň se rychle šíří od bytu v 3. patře. Hasiči evakuují 45 osob. Hrozba kolapsu budovy.",
        "type": "požár",
        "severity_range": (4, 5),
        "locations": [2],
    },
    {
        "title": "Zdravotnický nouzový stav v Plzni",
        "description": "Nemocnice přeplněná pacienty s toxickou otravou. Původ neznámý. Vyhlášen stav nouze.",
        "type": "zdravotnické_nouzové",
        "severity_range": (3, 4),
        "locations": [3],
    },
    {
        "title": "Průmyslová havárie v Liberci",
        "description": "Chemické zařízení exploze na okraji města. Toxické výpary se šíří nad okolí. Evakuace 500 osob.",
        "type": "průmyslová_havárie",
        "severity_range": (5, 5),
        "locations": [4],
    },
    {
        "title": "Teroristický útok na nádraží v Olomouci",
        "description": "Několik osob napadlo cestující. Jeden útočník zbrojí. Uzavření nádraží, zásah policie.",
        "type": "teroristický_útok",
        "severity_range": (4, 5),
        "locations": [5],
    },
    {
        "title": "Únos taxidáře v Českých Budějovicích",
        "description": "Ozbrojený podezřelý unáší taxidáře. Auto jedoucí na sever. Stav není znám.",
        "type": "únos",
        "severity_range": (4, 5),
        "locations": [6],
    },
    {
        "title": "Výpadek elektřiny v Hradci Králové",
        "description": "Rozsáhlý blackout v polovině města. Metrobus zastaveno, nemocnice na nouzovém režimu.",
        "type": "ostatní",
        "severity_range": (3, 4),
        "locations": [7],
    },
    {
        "title": "Havárie osobního vlaku u Pardubic",
        "description": "Vlak vykolejil na mostě. Desítky zraněných. Záchranáři v akci.",
        "type": "dopravní_nehoda",
        "severity_range": (4, 5),
        "locations": [8],
    },
    {
        "title": "Větví stromů blokují silnici",
        "description": "Silný vítr způsobil pád velkého stromu na D7. Silnice zablokovaná. Riziko dalších stromů.",
        "type": "přírodní_katastrofa",
        "severity_range": (2, 3),
        "locations": [9],
    },
    {
        "title": "Otrávená voda v Kladně",
        "description": "Bakteriologická kontaminace vodovodní sítě. 5000 lidí bez pitné vody.",
        "type": "zdravotnické_nouzové",
        "severity_range": (3, 4),
        "locations": [10],
    },
    {
        "title": "Průnik ropného zbytku do řeky Labe",
        "description": "Průmyslová výroba uvolnila toxickou tekutinu. Řeka Labe znečištěna na 20 km.",
        "type": "průmyslová_havárie",
        "severity_range": (4, 4),
        "locations": [11],
    },
    {
        "title": "Zemětřesení v Táboře",
        "description": "Překvapivé zemětřesení intenzity 4.5. Poškozeny historické budovy. Drobné škody na sítích.",
        "type": "přírodní_katastrofa",
        "severity_range": (2, 3),
        "locations": [12],
    },
    {
        "title": "Lesní požár v Chebu",
        "description": "Neplánitelný lesní požár. Hasiči ze čtyř okresů na místě. Evakuace okolních vesnic.",
        "type": "požár",
        "severity_range": (3, 4),
        "locations": [13],
    },
    {
        "title": "Krach staveniště v Modelové",
        "description": "Nezajištěné stavební lešení se zřítilo. 3 pracovníci zraněni, jeden mrtvý.",
        "type": "průmyslová_havárie",
        "severity_range": (3, 4),
        "locations": [14],
    },
    {
        "title": "Střelba na ulici v Praze",
        "description": "Neznámý útočník střílí na lidi na Václavském náměstí. Více raněných. Policie pátrá.",
        "type": "teroristický_útok",
        "severity_range": (5, 5),
        "locations": [0],
    },
    {
        "title": "Odsun pacienta s nakažlivou nemocí",
        "description": "Pacient s neznámou nemocí transportován do nemocnice. Uzavřena část města.",
        "type": "zdravotnické_nouzové",
        "severity_range": (3, 4),
        "locations": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    },
    {
        "title": "Strhávání ledovců na severu Čech",
        "description": "Ledovik se strhává. Hrozí povodně v údolí. Místní obyvatelé evakuováni.",
        "type": "přírodní_katastrofa",
        "severity_range": (3, 4),
        "locations": [4, 11],
    },
    {
        "title": "Plyn unikající z elektrárny",
        "description": "Stanice v vytváří nebezpečný únik. Evakuace části čtvrti.",
        "type": "průmyslová_havárie",
        "severity_range": (3, 3),
        "locations": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    },
    {
        "title": "Bouřka se připravuje - varování",
        "description": "Meteorologové varují před bouří s nebezpečnými větry až 120 km/h.",
        "type": "přírodní_katastrofa",
        "severity_range": (2, 4),
        "locations": [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],
    },
]


def fill_db(count: int = 20) -> None:
    """
    Naplní databázi <count> testovacími krizami.
    
    Parametry:
        count: Počet krizí k vygenerování (default 20)
    """
    # Získej connection strings z environment
    mongo_uri = os.environ.get("MONGO_URI", "mongodb://admin:admin@localhost:27017/krizove_udalosti?authSource=admin")
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    db_name = "krizove_udalosti"
    
    db = DatabaseManager(mongo_uri=mongo_uri, redis_url=redis_url, db_name=db_name)
    
    print(f"\n{'='*60}")
    print(f"Naplňování databáze {count} testovacími krizami...")
    print(f"{'='*60}\n")
    
    created_count = 0
    
    try:
        for i in range(count):
            # Vyber náhodný template
            template = CRISIS_TEMPLATES[i]
            
            # Vyber náhodné místo z těch, která se hodí pro tento typ
            loc_idx = random.choice(template["locations"])
            location_name, lat, lon = CZECH_LOCATIONS[loc_idx]
            
            # Severity - realistické rozložení
            severity = random.randint(*template["severity_range"])
            
            # Čas - poslední 7 dní
            hours_ago = random.randint(0, 168)
            created_at = datetime.now() - timedelta(hours=hours_ago)
            
            # Vytvoř event
            event = CrisisEvent(
                title=template["title"],
                description=template["description"],
                location=location_name,
                severity=severity,
                event_type=template["type"],
                latitude=lat,
                longitude=lon,
                created_at=created_at,
            )
            
            # Ulož do databáze
            try:
                event_id = db.create_event(event)
                created_count += 1
                
                severity_emoji = ["", "🟢", "🟡", "🟠", "🔴", "⚫"][severity]
                print(
                    f"  {created_count:2d}. {severity_emoji} {template['title']:<40} "
                    f"({location_name.split(',')[0]})"
                )
            except Exception as e:
                print(f"  ❌ Chyba při vytváření eventu: {e}")
                continue
        
        # Výstup - statistika
        print(f"\n{'='*60}")
        print(f"  ✅ Úspěšně vytvořeno: {created_count}/{count} krizí")
        
        # Zobraz statistiku
        try:
            stats = db.get_stats()
            print(f"\n  📊 Statistika databáze:")
            print(f"     • Celkem krizí: {stats['total_events']}")
            print(f"     • Kritické (sev. 5): {stats['by_severity'].get(5, 0)}")
            print(f"     • Vážné (sev. 4): {stats['by_severity'].get(4, 0)}")
            print(f"     • Střední (sev. 3): {stats['by_severity'].get(3, 0)}")
            print(f"     • Nižší (sev. 1-2): {stats['by_severity'].get(1, 0) + stats['by_severity'].get(2, 0)}")
        except:
            pass
        
        print(f"\n Aplikace je připravena! localhost:5000")
        print(f"{'='*60}\n")
    
    except Exception as e:
        print(f"\n❌ Kritická chyba: {e}")
        raise


if __name__ == "__main__":
    fill_db(20)
