# scripts/admin.py
# Usage:
#   python scripts/admin.py create-user email password
#   python scripts/admin.py change-password email newpassword
#   python scripts/admin.py list-users
#   python scripts/admin.py deactivate-user email
#   python scripts/admin.py activate-user email

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.db import SessionLocal, Base, engine
from backend.app.models.users import User
from backend.app.services.auth import hash_password

Base.metadata.create_all(bind=engine)


def create_user(email: str, password: str):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print("❌ User '{}' already exists.".format(email))
            return
        if len(password) < 6:
            print("❌ Password must be at least 6 characters.")
            return
        new_user = User(email=email, hashed_password=hash_password(password), is_active=True)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print("✅ User created successfully!")
        print("   ID:     {}".format(new_user.id))
        print("   Email:  {}".format(new_user.email))
        print("   Active: {}".format(new_user.is_active))
    except Exception as e:
        db.rollback()
        print("❌ Error: {}".format(e))
    finally:
        db.close()


def change_password(email: str, new_password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print("❌ User '{}' not found.".format(email))
            return
        if len(new_password) < 6:
            print("❌ Password must be at least 6 characters.")
            return
        user.hashed_password = hash_password(new_password)
        db.commit()
        print("✅ Password changed successfully for '{}'.".format(email))
    except Exception as e:
        db.rollback()
        print("❌ Error: {}".format(e))
    finally:
        db.close()


def list_users():
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.created_at).all()
        if not users:
            print("No users found.")
            return
        print("\n{:<5} {:<35} {:<10} {}".format("ID", "Email", "Active", "Created"))
        print("-" * 70)
        for u in users:
            created = u.created_at.strftime("%Y-%m-%d %H:%M") if u.created_at else "N/A"
            active = "✅ Yes" if u.is_active else "❌ No"
            print("{:<5} {:<35} {:<10} {}".format(u.id, u.email, active, created))
        print()
    except Exception as e:
        print("❌ Error: {}".format(e))
    finally:
        db.close()


def set_active(email: str, active: bool):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print("❌ User '{}' not found.".format(email))
            return
        user.is_active = active
        db.commit()
        status = "activated" if active else "deactivated"
        print("✅ User '{}' {}.".format(email, status))
    except Exception as e:
        db.rollback()
        print("❌ Error: {}".format(e))
    finally:
        db.close()


def print_help():
    print("""
WordApp Admin CLI
-----------------
Commands:
  create-user <email> <password>       Create a new user
  change-password <email> <password>   Change a user's password
  list-users                           List all users
  deactivate-user <email>              Block a user from logging in
  activate-user <email>                Re-enable a blocked user
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)

    command = sys.argv[1]

    if command == "create-user":
        if len(sys.argv) != 4:
            print("Usage: python scripts/admin.py create-user <email> <password>")
            sys.exit(1)
        create_user(sys.argv[2], sys.argv[3])

    elif command == "change-password":
        if len(sys.argv) != 4:
            print("Usage: python scripts/admin.py change-password <email> <password>")
            sys.exit(1)
        change_password(sys.argv[2], sys.argv[3])

    elif command == "list-users":
        list_users()

    elif command == "deactivate-user":
        if len(sys.argv) != 3:
            print("Usage: python scripts/admin.py deactivate-user <email>")
            sys.exit(1)
        set_active(sys.argv[2], False)

    elif command == "activate-user":
        if len(sys.argv) != 3:
            print("Usage: python scripts/admin.py activate-user <email>")
            sys.exit(1)
        set_active(sys.argv[2], True)

    else:
        print("❌ Unknown command: '{}'".format(command))
        print_help()
        sys.exit(1)
