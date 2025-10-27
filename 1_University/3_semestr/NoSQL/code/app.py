from flask import Flask, render_template, request, redirect, session
import os
import json
import redis


# app = Flask(__name__)

# kocky = [
#     {
#         "jmeno": "minda",
#         "barva srsti": "rezava",
#         "vek": 2
#     },
#     {
#         "jmeno": "linda",
#         "barva srsti": "cerna",
#         "vek": 5
#     },
#     {
#         "jmeno": "pinda",
#         "barva srsti": "strakata",
#         "vek": 17
#     },
#     {
#         "jmeno": "zbynda",
#         "barva srsti": "bílá",
#         "vek": 10
#     }
# ]

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "dev-secret-change-me")

# Redis connection (v Docker Compose je service jméno 'redis')
REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(REDIS_URL, decode_responses=True)
#r = redis.Redis(host="redis", port=6379)
# default data (used only to initialize Redis if empty)
DEFAULT_CATS = [
    {"jmeno": "minda", "barva_srsti": "rezava", "vek": 2},
    {"jmeno": "linda", "barva_srsti": "cerna", "vek": 5},
    {"jmeno": "pinda", "barva_srsti": "strakata", "vek": 17},
    {"jmeno": "zbynda", "barva_srsti": "bila", "vek": 10},
]

def load_cats():
    raw = r.get("cats")
    if not raw:
        # initialize
        r.set("cats", json.dumps(DEFAULT_CATS))
        return DEFAULT_CATS.copy()
    try:
        return json.loads(raw)
    except Exception:
        return DEFAULT_CATS.copy()

def save_cats(cats):
    r.set("cats", json.dumps(cats))

# track global page views and per-session per-page visits
@app.before_request
def track_visits():
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