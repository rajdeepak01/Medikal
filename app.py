import os
from flask import Flask, send_from_directory
from backend.database import db
from datetime import timedelta
from dotenv import load_dotenv
from flask_migrate import Migrate

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Initialize Flask app
app = Flask(__name__, static_folder='static')

# ✅ Static file routes
@app.route('/sitemap.xml', endpoint='sitemap_static')
def sitemap():
    return send_from_directory(app.static_folder, 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/google0bd79030d3228202.html')
def google_verification():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'google0bd79030d3228202.html')

# ✅ Always use SQLite (local db.sqlite3 file in project root)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ Session configuration
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key")  
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)
app.config["SESSION_COOKIE_NAME"] = "yourdr_session"
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False  # Set to True in production with HTTPS

# ✅ Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# ✅ Import routes inside app context
with app.app_context():
    from backend import controllers
    # db.create_all()  # Optional: uncomment for first-time setup

# ✅ Run app
if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "True")
