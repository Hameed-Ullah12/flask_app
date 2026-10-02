from flask import Flask
from config import Config
from extensions import db, login_manager
from controllers.auth_controller import auth
from models.user_model import User
from controllers.product_controller import product 

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth)
app.register_blueprint(product)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
