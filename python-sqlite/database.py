from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum
import os

Base = declarative_base()

# Use SQLite for local development and production
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///theater_booking.db')
engine = create_engine(DATABASE_URL, echo=False)

class ScreenType(enum.Enum):
    GOLD = "gold"
    MAX = "max"
    GENERAL = "general"

class Theater(Base):
    __tablename__ = 'theaters'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    location = Column(String(100))
    screens = relationship("Screen", back_populates="theater")

class Screen(Base):
    __tablename__ = 'screens'
    id = Column(Integer, primary_key=True)
    theater_id = Column(Integer, ForeignKey('theaters.id'))
    screen_type = Column(Enum(ScreenType))
    total_seats = Column(Integer)
    movie_name = Column(String(100))
    show_time = Column(DateTime)
    theater = relationship("Theater", back_populates="screens")
    bookings = relationship("Booking", back_populates="screen")

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    screen_id = Column(Integer, ForeignKey('screens.id'))
    user_name = Column(String(100))
    seat_number = Column(Integer)
    booking_time = Column(DateTime, default=datetime.now)
    is_cancelled = Column(Boolean, default=False)
    has_food = Column(Boolean, default=False)
    screen = relationship("Screen", back_populates="bookings")
    food_orders = relationship("FoodOrder", back_populates="booking")

class WaitingList(Base):
    __tablename__ = 'waiting_list'
    id = Column(Integer, primary_key=True)
    screen_id = Column(Integer, ForeignKey('screens.id'))
    user_name = Column(String(100))
    request_time = Column(DateTime, default=datetime.now)

class FoodOrder(Base):
    __tablename__ = 'food_orders'
    id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'))
    item_name = Column(String(50))
    quantity = Column(Integer)
    price = Column(Float)
    booking = relationship("Booking", back_populates="food_orders")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)