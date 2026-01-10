# Movie Booking System (Python & SQLite)

## Overview
A theater booking system that allows users to book movie tickets, view current bookings, and order food items. It provides multiple interfaces including a modern web-based Streamlit app that's ready for cloud deployment.

## Features

- **Theater Booking**: Book tickets for different theaters and screen types (Gold, IMAX, and General)
- **Food Orders**: Order food items like popcorn and sandwiches with price discounts based on screen type
- **Waiting List**: If the screen is full, users are added to a waiting list and notified when a seat becomes available
- **Cancel Bookings**: Cancel tickets (if the show is more than 30 minutes away)
- **User-Friendly UI**: Interactive web interface for booking and viewing bookings

---

## Quick Start

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd python-sqlite
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

3. **Access the app**: Open your browser to `http://localhost:8501`

## Deploy to Render

1. **Fork this repository** to your GitHub account

2. **Connect to Render**:
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `python-sqlite` folder as the root directory

3. **Configure the service**:
   - **Name**: `movie-booking-system` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false`

4. **Deploy**: Click "Create Web Service" and wait for deployment to complete

**Alternative**: Use the included `render.yaml` file for automatic configuration.

The app will automatically:
- Create a SQLite database
- Initialize with sample theater and movie data
- Be accessible via your Render URL

---

## Technical Details

- **Database**: SQLite (production-ready, no setup required)
- **Backend**: SQLAlchemy ORM with Python
- **Frontend**: Streamlit web framework
- **Deployment**: Render-ready with automatic database initialization

## Screenshots

### Streamlit Web App
![Streamlit](images/streamlit.jpg)

### CLI Interface
![CLI](images/cli.jpg)

### GUI Interface
![GUI](images/gui.jpg)

---

## Environment Variables

For production deployment, you can optionally set:
- `DATABASE_URL`: Custom database URL (defaults to SQLite)
- `PORT`: Server port (automatically set by Render)

## License

This project is licensed under the MIT License.
