from flask import Flask, jsonify, request
from flask_cors import CORS
from config import ApplicationConfig
from app.models import db, User, UserRole, Invoice, Supplier, Buyer
from app.organizations import organizations_bp
from app.getData import getData_bp
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.config.update(ENV='development')
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, supports_credentials=True)
app.register_blueprint(organizations_bp)
app.register_blueprint(getData_bp)
bcrypt = Bcrypt()

db.init_app(app)

# Hardcoded email and password
CONSTANT_EMAIL = 'admin@example.com'
CONSTANT_PASSWORD = 'admin_password'

with app.app_context():
    db.create_all()

    # Check if the default user exists, create if not
    admin_user = User.query.filter_by(email=CONSTANT_EMAIL).first()
    if not admin_user:
        hashed_password = bcrypt.generate_password_hash(CONSTANT_PASSWORD).decode('utf-8')
        admin_user = User(email=CONSTANT_EMAIL, name='Admin', password=hashed_password)
        admin_user.role = UserRole.ADMIN
        db.session.add(admin_user)
        db.session.commit()

# Route to get user information without authentication
@app.route("/@me")
def get_current_user():
    # Simulate authentication using the hardcoded email and password
    if request.authorization and \
       request.authorization.username == CONSTANT_EMAIL and \
       bcrypt.check_password_hash(admin_user.password, request.authorization.password):
        return jsonify({
            "name": admin_user.name,
            "email": admin_user.email,
            "role": admin_user.role.value
        })
    else:
        return jsonify({"error": "Unauthorized"}), 401

# Other routes without authentication

if __name__ == "__main__":
    app.run(debug=True)
