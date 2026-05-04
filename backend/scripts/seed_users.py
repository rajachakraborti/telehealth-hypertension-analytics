#!/usr/bin/env python3
"""
Seed script to create sample users for the Telehealth Hypertension Analytics System.

Usage:
    cd backend
    python scripts/seed_users.py

This will create test users with the following credentials:
    - admin / admin123
    - testuser / test123
    - clinician / clinic123
    - analyst / analyst123
"""

import sys
import os

# Add the parent directory to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User, Base
from app.core.security import get_password_hash

# Database URL - update this if your config is different
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://username:password@localhost:5432/telehealth_db"
)

def seed_users():
    """Create sample users with hashed passwords."""

    # Create engine and session
    engine = create_engine(DATABASE_URL)

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Sample users with plain text passwords (will be hashed)
    sample_users = [
        {
            "username": "admin",
            "email": "admin@example.com",
            "password": "admin123",
            "is_superuser": True,
            "is_active": True
        },
        {
            "username": "testuser",
            "email": "test@example.com",
            "password": "test123",
            "is_superuser": False,
            "is_active": True
        },
        {
            "username": "clinician",
            "email": "clinician@example.com",
            "password": "clinic123",
            "is_superuser": False,
            "is_active": True
        },
        {
            "username": "analyst",
            "email": "analyst@example.com",
            "password": "analyst123",
            "is_superuser": False,
            "is_active": True
        },
    ]

    created_count = 0
    skipped_count = 0

    for user_data in sample_users:
        # Check if user already exists
        existing_user = db.query(User).filter(
            User.username == user_data["username"]
        ).first()

        if existing_user:
            print(f"User '{user_data['username']}' already exists, skipping...")
            skipped_count += 1
            continue

        # Create new user with hashed password
        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            hashed_password=get_password_hash(user_data["password"]),
            is_superuser=user_data["is_superuser"],
            is_active=user_data["is_active"]
        )

        db.add(new_user)
        print(f"Created user: {user_data['username']} (password: {user_data['password']})")
        created_count += 1

    db.commit()
    db.close()

    print(f"\n{'='*50}")
    print(f"Seeding complete!")
    print(f"Created: {created_count} users")
    print(f"Skipped: {skipped_count} users (already existed)")
    print(f"{'='*50}")
    print("\nYou can now login with these credentials:")
    print("  Username: admin      Password: admin123")
    print("  Username: testuser   Password: test123")
    print("  Username: clinician  Password: clinic123")
    print("  Username: analyst    Password: analyst123")


if __name__ == "__main__":
    try:
        seed_users()
    except Exception as e:
        print(f"Error seeding users: {e}")
        print("\nMake sure:")
        print("1. PostgreSQL is running")
        print("2. The database 'telehealth_db' exists")
        print("3. DATABASE_URL environment variable is set correctly")
        sys.exit(1)
