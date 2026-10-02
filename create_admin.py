from app import app
from models.user_model import User
from extensions import db
from getpass import getpass


def create_admin():
    with app.app_context():

        print("=== Create Admin Account===")

        username = input("Enter admin username:").strip()
        email = input("Enter admin email:").strip()

        password = getpass("Enter admin password: ")
        confirm_password = getpass("Confirm admin password:")

        if password != confirm_password:
            print("Error: Password do not match.")
            return

        if len(password) <6:
            print("Error: Password must be at least 6 characters.")
            return

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            print("Error: User with this email already exists.")
            return

        admin = User(
            username=username,
            email=email,
            role="admin"
        )

        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        print("\nAdmin account created successfully.")
        print(f"Username: {username}")
        print(f"Email: {email}")

if __name__ == "__main__":
    create_admin()
