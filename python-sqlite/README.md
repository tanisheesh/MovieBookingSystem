# Movie Booking System (Python & SQLite)

## 🎬 Live Demo
**🚀 [Try the Live App](https://moviebookingsystem-iztj.onrender.com/)**

## Overview
A modern theater booking system that allows users to book movie tickets, view current bookings, and order food items. Features a sleek web interface with real-time pricing, waiting list management, and automatic seat assignment.

## ✨ Features

- **🎫 Smart Booking System**: Book tickets for different theaters and screen types (Gold, IMAX, General)
- **🍿 Food Ordering**: Order popcorn and sandwiches with automatic discounts based on screen type
- **⏳ Intelligent Waiting List**: Automatic seat assignment when cancellations occur
- **💰 Real-time Pricing**: Live price updates as you add food items
- **📱 Responsive Design**: Works perfectly on desktop and mobile
- **🔄 Live Updates**: Real-time availability and booking status

## 🎯 Screen Types & Pricing

| Screen Type | Seats | Ticket Price | Food Discount |
|-------------|-------|--------------|---------------|
| **Gold** 🥇 | 2 seats | ₹400 | 10% off food |
| **IMAX** 🎭 | 5 seats | ₹300 | 5% off food |
| **General** 🎪 | 10 seats | ₹200 | No discount |

## 🍿 Food Menu
- **Popcorn**: ₹150 per serving
- **Sandwich**: ₹100 per serving


## 🚀 Quick Start

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd python-sqlite
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   streamlit run app.py
   ```

3. **Access**: Open `http://localhost:8501`

## 🧪 How to Test

### Test the Waiting List Feature:
1. **Fill Gold seats** (book 2 tickets) → 3rd person goes to waiting list
2. **Cancel a Gold booking** → Waiting list person automatically gets confirmed
3. **Check waiting list section** → See who's waiting and their position

### Test Real-time Pricing:
1. **Select screen type** → See base ticket price
2. **Add food items** → Watch total price update instantly
3. **Try different screen types** → See discount percentages change

### Test Booking Flow:
1. **Select theater and screen type**
2. **Check availability** (Available/Total seats shown)
3. **Enter your name**
4. **Add food items** (optional)
5. **See price breakdown** with discounts
6. **Book ticket** → Get confirmation with seat number

## 🛠 Technical Details

- **Database**: SQLite (production-ready, no setup required)
- **Backend**: SQLAlchemy 1.4 ORM with Python 3.11
- **Frontend**: Streamlit web framework
- **Deployment**: Render-ready with automatic database initialization
- **Features**: Real-time updates, session management, error handling

## 📄 License

This project is licensed under the MIT License.