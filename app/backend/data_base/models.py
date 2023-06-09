from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

    images = relationship("Image", back_populates="owner")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phash = Column(String)
    size = Column(Float)
    date = Column(DateTime)
    content = Column(String)
    smallRoundContent = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="images")

    gps_id = Column(Integer, ForeignKey("gps.id"), nullable=True)
    gps = relationship(
        "GPS", back_populates="image", cascade="all, delete-orphan", single_parent=True
    )

    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    location = relationship(
        "Location",
        back_populates="image",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    __table_args__ = (UniqueConstraint("gps_id", "location_id"),)


class GPS(Base):
    __tablename__ = "gps"
    id = Column(Integer, primary_key=True, index=True)
    altitude = Column(Float)
    direction = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)

    image = relationship(
        "Image", uselist=False, back_populates="gps", cascade="all, delete-orphan"
    )


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    data = Column(String)

    image = relationship(
        "Image", uselist=False, back_populates="location", cascade="all, delete-orphan"
    )
