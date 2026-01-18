import os
from flask import Flask, send_from_directory
from backend.database import db
from datetime import timedelta
from dotenv import load_dotenv
from flask_migrate import Migrate

load_dotenv()

app = Flask(__name__, static_folder='static')


# ---------------------------
# 🌐 STATIC ROUTES
# ---------------------------

@app.route('/sitemap.xml', endpoint='sitemap_static')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/google0bd79030d3228202.html')
def google_verification():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'google0bd79030d3228202.html'
    )


# ---------------------------
# 💾 DATABASE CONFIG (RENDER LOCAL INSTANCE)
# ---------------------------

RENDER = os.getenv("RENDER")

if RENDER:
    # Render allows writes inside its own project directory
    DB_DIR = "/opt/render/project/src/data"
    os.makedirs(DB_DIR, exist_ok=True)
    DB_PATH = os.path.join(DB_DIR, "db.sqlite3")

    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
    print(f"Using Render instance DB at: {DB_PATH}")

else:
    # Local dev
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# ---------------------------
# 🔐 SESSION CONFIG
# ---------------------------

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key")
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)
app.config["SESSION_COOKIE_NAME"] = "yourdr_session"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = bool(RENDER)


# ---------------------------
# 🗄️ DB INIT + MIGRATIONS
# ---------------------------

db.init_app(app)
migrate = Migrate(app, db)


# ---------------------------
# 📦 SAFE AUTO TABLE CREATION
# ---------------------------

with app.app_context():
    from backend import controllers
    try:
        db.create_all()
        print("✔ Database initialized")
    except Exception as e:
        print("❌ DB Init Error:", e)


# ---------------------------
# 🚀 LOCAL DEV ENTRYPOINT
# ---------------------------

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG") == "True"
    app.run(debug=debug)
