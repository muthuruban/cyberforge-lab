"""Simple application models for StaffHub."""

from dataclasses import dataclass


@dataclass(slots=True)
class StaffUser:
    """Represents a seeded StaffHub user."""

    id: int
    full_name: str
    role: str
    email: str
    password: str
    department: str
