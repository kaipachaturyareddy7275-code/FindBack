from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(String(150), unique=True, nullable=False, index=True)

    password = Column(String(255), nullable=False)

    student_id = Column(String(50), unique=True, nullable=True)

    role = Column(String(20), default="student")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    type = Column(String(10), nullable=False)

    name = Column(String(100), nullable=False)

    category = Column(String(50), nullable=False)

    description = Column(Text, nullable=True)

    image_url = Column(String(255), nullable=True)

    location = Column(String(100), nullable=False)

    specific_location = Column(String(200), nullable=True)

    date = Column(String(20), nullable=False)

    start_time = Column(String(20), nullable=True)

    end_time = Column(String(20), nullable=True)

    status = Column(
        String(20),
        default="active"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )