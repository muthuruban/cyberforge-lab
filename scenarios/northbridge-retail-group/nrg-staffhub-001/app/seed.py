"""Seed data for StaffHub lab scenario."""

from __future__ import annotations

from database import get_connection, init_database

SEED_USERS = [
    {
        "full_name": "Maya Patel",
        "role": "SOC Analyst",
        "email": "maya.patel@northbridge.test",
        "password": "Northbridge!123",
        "department": "Security Operations",
    },
    {
        "full_name": "Ethan Brooks",
        "role": "IT Support Engineer",
        "email": "ethan.brooks@northbridge.test",
        "password": "Helpdesk!2024",
        "department": "IT Support",
    },
    {
        "full_name": "Priya Nair",
        "role": "HR Manager",
        "email": "priya.nair@northbridge.test",
        "password": "PeopleOps!11",
        "department": "Human Resources",
    },
    {
        "full_name": "Oliver Reed",
        "role": "Store Operations Lead",
        "email": "oliver.reed@northbridge.test",
        "password": "Stores!445",
        "department": "Store Operations",
    },
    {
        "full_name": "Lena Morris",
        "role": "Finance Assistant",
        "email": "lena.morris@northbridge.test",
        "password": "Finance!889",
        "department": "Finance",
    },
    {
        "full_name": "Samir Khan",
        "role": "Application Developer",
        "email": "samir.khan@northbridge.test",
        "password": "DevTeam!778",
        "department": "Engineering",
    },
]


def seed_if_needed() -> None:
    """Insert initial users if database is empty."""
    init_database()
    with get_connection() as conn:
        result = conn.execute("SELECT COUNT(*) AS count FROM users").fetchone()
        if result and result["count"] > 0:
            return

        for user in SEED_USERS:
            conn.execute(
                """
                INSERT INTO users (full_name, role, email, password, department)
                VALUES (:full_name, :role, :email, :password, :department)
                """,
                user,
            )
        conn.commit()


if __name__ == "__main__":
    seed_if_needed()
