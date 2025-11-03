from flask import Flask, render_template, request, redirect, session
import os
import json
import redis
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-change-me")


# Redis connection (v Docker Compose je service jméno 'redis')
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
# r = redis.from_url(REDIS_URL, decode_responses=True)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/mydb") 
# client = MongoClient(MONGO_URI) 
# db = client.get_database()
# cats_col = db.cats

# lazy globals (nevytvářet klienty při importu — zabraňuje problémům s reloaderem na Windows)
r = None
client = None
db = None
cats_col = None


def init_stores():
    """
    Lazy init Redis + Mongo clients. Volat uvnitř request/pri prvním použití,
    aby se nespouštěly background threads/sockets při importu (debug reloader issue).
    """
    global r, client, db, cats_col
    if r is None:
        try:
            r = redis.from_url(REDIS_URL, decode_responses=True)
        except Exception:
            r = None
    if client is None:
        try:
            client = MongoClient(MONGO_URI)
            db = client.get_database()
            cats_col = db.cats
        except Exception:
            client = None
            db = None
            cats_col = None

#r = redis.Redis(host="redis", port=6379)
# default data (used only to initialize Redis if empty)
DEFAULT_CATS = [
    {"jmeno": "minda", "barva_srsti": "rezava", "vek": 2},
    {"jmeno": "linda", "barva_srsti": "cerna", "vek": 5},
    {"jmeno": "pinda", "barva_srsti": "strakata", "vek": 17},
    {"jmeno": "zbynda", "barva_srsti": "bila", "vek": 10},
]

CACHE_TTL = 5  # seconds

def load_cats():
    """
    Cache-aside: try Redis key "cats_cache". If miss, load from persistent source
    (here DEFAULT_CATS or other DB), populate cache with TTL and return.
    """
    try:
        raw = r.get("cats_cache")
    except Exception:
        raw = None

    if raw:
        try:
            return json.loads(raw)
        except Exception:
            # broken cache entry: remove and fall through to authoritative source
            try:
                r.delete("cats_cache")
            except Exception:
                pass

    # cache miss -> načti z MongoDB
    try:
        if cats_col:
            docs = list(cats_col.find({}, {"_id": 0}))
        else:
            docs = []
        if not docs:
            cats = DEFAULT_CATS.copy()
            try:
                if cats_col:
                    cats_col.insert_many(cats)
            except Exception:
                pass
        else:
            cats = docs
    except Exception:
        cats = DEFAULT_CATS.copy()

    try:
        if r:
            r.set("cats_cache", json.dumps(cats), ex=CACHE_TTL)
    except Exception:
        pass

    return cats

def save_cats(cats):
    init_stores()
    """
    Persist list of cats to MongoDB (replace collection contents) and update Redis cache.
    """
    try:
        if cats_col:
            cats_col.delete_many({})
            if cats:
                cats_col.insert_many(cats)
    except Exception:
        pass

    try:
        if r:
            r.set("cats_cache", json.dumps(cats), ex=CACHE_TTL)
    except Exception:
        pass


# track global page views and per-session per-page visits
@app.before_request
def track_visits():
    init_stores()
    # skip static files
    if request.path.startswith("/static"):
        return
    try:
        r.incr("counter:global")
    except Exception:
        pass
    key = f"visits:{request.path}"
    session[key] = session.get(key, 0) + 1

@app.context_processor
def inject_counters():
    init_stores()
    # page_visits from session, global_count from Redis
    try:
        page_visits = session.get(f"visits:{request.path}", 0)
    except Exception:
        page_visits = 0
    try:
        global_count = int(r.get("counter:global") or 0)
    except Exception:
        global_count = 0
    return dict(page_visits=page_visits, global_count=global_count)



@app.route("/")
@app.route("/home")
def zobraz_home():
    return render_template("home.html")

@app.route("/seznamkocek")
def zobraz_kocky():
    cats = load_cats()
    return render_template("kocky.html", data=cats)

@app.route("/kontakt", methods=["GET", "POST"])
def zobraz_kontaktni_formular():
    if request.method == "GET":
        return render_template("kontakt.html")
    # -------
    jmeno = request.form.get("jmeno", "").strip()
    barva_srsti = request.form.get("barva_srsti", "").strip()
    vek = request.form.get("vek", "").strip()
    try:
        vek_int = int(vek)
    except Exception:
        vek_int = vek
    cats = load_cats()
    cats.append({"jmeno": jmeno, "barva_srsti": barva_srsti, "vek": vek_int})
    save_cats(cats)
    return redirect("/seznamkocek")
    # elif request.method == "POST":
    #     jmeno = request.form["jmeno"]
    #     barva_srsti = request.form["barva srsti"]
    #     vek = request.form["vek"]
    #     kocky.append(
    #         {
    #             "jmeno": jmeno,
    #             "barva srsti": barva_srsti,
    #             "vek": vek
    #         }
    #     )
    #     return redirect("/seznamkocek")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)