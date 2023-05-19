from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, server_default="user", nullable=True)

    booking = relationship("Bookings", back_populates="user_email")

    def __str__(self) -> str:
        return f"{self.email}"
