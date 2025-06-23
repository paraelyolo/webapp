from flask import Flask
from routes.login import login_bp
from routes.dashboard import dashboard_bp
from routes.log import log_bp

app = Flask(__name__)
app.secret_key = 'superclave'  # cambiala en produccion

# Registrar los blueprints
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(log_bp)

if __name__ == "__main__":
    app.run(debug=True)
