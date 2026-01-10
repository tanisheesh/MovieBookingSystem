import streamlit as st
import os
from datetime import datetime, timedelta
from database import Session, Theater, Screen, ScreenType, Booking, WaitingList, Base, engine
from booking_system import BookingSystem

def initialize_database():
    """Initialize database if it doesn't exist"""
    Base.metadata.create_all(engine)
    
    session = Session()
    try:
        existing_theaters = session.query(Theater).count()
        
        if existing_theaters == 0:
            # Add sample data with correct seat limits
            theaters = [
                Theater(name="PVR Cinemas", location="Mumbai"),
                Theater(name="INOX", location="Delhi"),
                Theater(name="Cinepolis", location="Bangalore")
            ]
            session.add_all(theaters)
            session.commit()
            
            for theater in theaters:
                screens = [
                    Screen(
                        theater_id=theater.id, 
                        screen_type=ScreenType.GOLD, 
                        total_seats=2,  # Gold: 2 seats
                        movie_name="Avengers: Endgame", 
                        show_time=datetime.now() + timedelta(hours=2)
                    ),
                    Screen(
                        theater_id=theater.id, 
                        screen_type=ScreenType.MAX, 
                        total_seats=5,  # IMAX: 5 seats
                        movie_name="Spider-Man: No Way Home", 
                        show_time=datetime.now() + timedelta(hours=3)
                    ),
                    Screen(
                        theater_id=theater.id, 
                        screen_type=ScreenType.GENERAL, 
                        total_seats=10,  # General: 10 seats
                        movie_name="The Batman", 
                        show_time=datetime.now() + timedelta(hours=1)
                    )
                ]
                session.add_all(screens)
            session.commit()
    finally:
        session.close()

def initialize():
    if 'booking_system' not in st.session_state:
        with st.spinner("Initializing database..."):
            initialize_database()
            st.session_state.booking_system = BookingSystem()

def calculate_and_display_price():
    """Calculate and display real-time pricing"""
    if not hasattr(st.session_state, 'theater') or not hasattr(st.session_state, 'screen_type'):
        return 0
    
    screen_type_map = {
        "GOLD (₹400)": ScreenType.GOLD,
        "IMAX (₹300)": ScreenType.MAX,
        "General (₹200)": ScreenType.GENERAL
    }
    
    screen_type = screen_type_map.get(st.session_state.screen_type)
    if not screen_type:
        return 0
    
    food_items = {}
    if hasattr(st.session_state, 'popcorn') and st.session_state.popcorn > 0:
        food_items['popcorn'] = st.session_state.popcorn
    if hasattr(st.session_state, 'sandwich') and st.session_state.sandwich > 0:
        food_items['sandwich'] = st.session_state.sandwich
    
    ticket_price, food_total, total_price = st.session_state.booking_system.calculate_total_price(
        screen_type, food_items
    )
    
    # Display pricing breakdown
    st.markdown("### 💰 Price Breakdown")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Ticket Price", f"₹{ticket_price}")
        if food_total > 0:
            discount_pct = {
                ScreenType.GOLD: "10%",
                ScreenType.MAX: "5%", 
                ScreenType.GENERAL: "0%"
            }[screen_type]
            st.metric("Food Total", f"₹{food_total:.0f}", f"{discount_pct} discount applied")
    
    with col2:
        st.metric("**Total Amount**", f"**₹{total_price:.0f}**")
    
    return total_price

def get_availability_info(theater_name, screen_type_display):
    """Get seat availability information"""
    session = Session()
    try:
        theater = session.query(Theater).filter(Theater.name == theater_name).first()
        if not theater:
            return 0, 0, 0
        
        screen_type_map = {
            "GOLD (₹400)": ScreenType.GOLD,
            "IMAX (₹300)": ScreenType.MAX,
            "General (₹200)": ScreenType.GENERAL
        }
        
        screen_type = screen_type_map[screen_type_display]
        available, total = st.session_state.booking_system.get_screen_availability(theater.id, screen_type)
        
        # Get waiting list count
        screen = session.query(Screen).filter(
            Screen.theater_id == theater.id,
            Screen.screen_type == screen_type
        ).first()
        
        waiting_count = 0
        if screen:
            waiting_count = session.query(WaitingList).filter(
                WaitingList.screen_id == screen.id
            ).count()
        
        return available, total, waiting_count
    finally:
        session.close()

def book_ticket():
    if not st.session_state.name:
        st.error("Please enter your name")
        return
    
    with st.spinner("Processing your booking..."):
        session = Session()
        try:
            theater = session.query(Theater).filter(
                Theater.name == st.session_state.theater
            ).first()
            
            screen_type_map = {
                "GOLD (₹400)": ScreenType.GOLD,
                "IMAX (₹300)": ScreenType.MAX,
                "General (₹200)": ScreenType.GENERAL
            }
            
            food_items = {}
            if st.session_state.popcorn > 0:
                food_items['popcorn'] = st.session_state.popcorn
            if st.session_state.sandwich > 0:
                food_items['sandwich'] = st.session_state.sandwich
            
            result, booking_id = st.session_state.booking_system.book_ticket(
                theater_id=theater.id,
                screen_type=screen_type_map[st.session_state.screen_type],
                user_name=st.session_state.name,
                food_items=food_items
            )
            
            if "successful" in result:
                st.success(f"🎉 {result} | Booking ID: {booking_id}")
            else:
                st.warning(f"⏳ {result}")
        finally:
            session.close()

def cancel_booking(booking_id):
    with st.spinner("Cancelling booking..."):
        result = st.session_state.booking_system.cancel_ticket(booking_id)
        st.info(result)

def display_waiting_list():
    """Display the waiting list"""
    waiting_list = st.session_state.booking_system.get_waiting_list()
    
    if waiting_list:
        st.subheader("⏳ Waiting List")
        for i, entry in enumerate(waiting_list, 1):
            session = Session()
            try:
                screen = session.query(Screen).get(entry.screen_id)
                theater = session.query(Theater).get(screen.theater_id)
                
                with st.expander(f"#{i} - {entry.user_name}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Theater:** {theater.name}")
                        st.write(f"**Movie:** {screen.movie_name}")
                    with col2:
                        st.write(f"**Screen:** {screen.screen_type.value.title()}")
                        st.write(f"**Requested:** {entry.request_time.strftime('%H:%M')}")
            finally:
                session.close()
    else:
        st.info("No one in waiting list currently")

def main():
    st.set_page_config(page_title="ShowTimeSync", layout="wide")
    initialize()
    
    st.title("🎬 ShowTimeSync")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.subheader("🎫 Book Your Show")
        
        session = Session()
        try:
            theaters = session.query(Theater).all()
            theater_names = [theater.name for theater in theaters]
        finally:
            session.close()
        
        st.selectbox("Select Theater", 
                    theater_names, 
                    key='theater')
        
        screen_type = st.selectbox("Screen Type",
                    ["GOLD (₹400)", "IMAX (₹300)", "General (₹200)"],
                    key='screen_type')
        
        # Show availability
        if hasattr(st.session_state, 'theater') and hasattr(st.session_state, 'screen_type'):
            available, total, waiting_count = get_availability_info(st.session_state.theater, st.session_state.screen_type)
            
            col_avail1, col_avail2, col_avail3 = st.columns(3)
            with col_avail1:
                st.metric("Available", f"{available}/{total}")
            with col_avail2:
                st.metric("Waiting", waiting_count)
            with col_avail3:
                status = "🟢 Available" if available > 0 else "🔴 Full"
                st.metric("Status", status)
        
        st.text_input("Your Name", key='name')
        
        st.subheader("🍿 Food & Beverages")
        col_food1, col_food2 = st.columns(2)
        with col_food1:
            st.number_input("Popcorn (₹150)", 
                          min_value=0, 
                          max_value=10, 
                          value=0,
                          key='popcorn')
        with col_food2:
            st.number_input("Sandwich (₹100)", 
                          min_value=0, 
                          max_value=10, 
                          value=0,
                          key='sandwich')
        
        # Real-time pricing
        total_price = calculate_and_display_price()
        
        if st.button("🎯 Book Now", type="primary", use_container_width=True):
            book_ticket()
            st.rerun()
    
    with col2:
        st.subheader("📋 Current Bookings")
        
        session = Session()
        try:
            bookings = session.query(Booking).filter(
                Booking.is_cancelled == False
            ).all()
        finally:
            session.close()
        
        if bookings:
            for booking in bookings:
                with st.expander(f"🎫 {booking.user_name} - ID: {booking.id}"):
                    session = Session()
                    try:
                        screen = session.query(Screen).get(booking.screen_id)
                        theater = session.query(Theater).get(screen.theater_id)
                        
                        col_book1, col_book2 = st.columns(2)
                        with col_book1:
                            st.write(f"**Theater:** {theater.name}")
                            st.write(f"**Movie:** {screen.movie_name}")
                        with col_book2:
                            st.write(f"**Screen:** {screen.screen_type.value.title()}")
                            st.write(f"**Seat:** {booking.seat_number}")
                        
                        if st.button("❌ Cancel Booking", 
                                   key=f"cancel_{booking.id}"):
                            cancel_booking(booking.id)
                            st.rerun()
                    finally:
                        session.close()
        else:
            st.info("No current bookings")
    
    with col3:
        display_waiting_list()
    
    st.markdown("---")
    st.markdown(
        "<h6 style='text-align: center;'>Made with ❤️ by Tanish Poddar</h6>", 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()