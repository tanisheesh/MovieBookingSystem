from datetime import datetime, timedelta
from database import Session, Theater, Screen, Booking, WaitingList, FoodOrder, ScreenType

class BookingSystem:
    def __init__(self):
        self.food_prices = {
            'popcorn': 150,
            'sandwich': 100
        }
        self.screen_prices = {
            ScreenType.GOLD: 400,
            ScreenType.MAX: 300,
            ScreenType.GENERAL: 200
        }
        self.food_discounts = {
            ScreenType.GOLD: 0.10,
            ScreenType.MAX: 0.05,
            ScreenType.GENERAL: 0
        }

    def get_session(self):
        """Get a fresh session for each operation"""
        return Session()

    def book_ticket(self, theater_id, screen_type, user_name, food_items=None):
        session = self.get_session()
        try:
            screen = session.query(Screen).filter(
                Screen.theater_id == theater_id,
                Screen.screen_type == screen_type
            ).first()
            
            if not screen:
                return ("Screen not found", None)
            
            booked_seats = session.query(Booking).filter(
                Booking.screen_id == screen.id,
                Booking.is_cancelled == False
            ).count()
            
            if booked_seats >= screen.total_seats:
                self._add_to_waiting_list(screen.id, user_name, session)
                return ("Screen full. Added to waiting list.", None)
            
            next_seat = booked_seats + 1
            booking = Booking(
                screen_id=screen.id,
                user_name=user_name,
                seat_number=next_seat,
                has_food=bool(food_items)
            )
            session.add(booking)
            session.flush()  # Get the booking ID
            
            if food_items:
                discount = self.food_discounts[screen_type]
                for item, quantity in food_items.items():
                    if quantity > 0:
                        price = self.food_prices[item] * quantity * (1 - discount)
                        food_order = FoodOrder(
                            booking_id=booking.id,
                            item_name=item,
                            quantity=quantity,
                            price=price
                        )
                        session.add(food_order)
            
            session.commit()
            return f"Booking successful. Seat number: {next_seat}", booking.id
            
        except Exception as e:
            session.rollback()
            return f"Booking failed: {str(e)}", None
        finally:
            session.close()

    def cancel_ticket(self, booking_id):
        session = self.get_session()
        try:
            booking = session.query(Booking).get(booking_id)
            if not booking:
                return "Booking not found"
            
            screen = booking.screen
            current_time = datetime.now()
            if current_time + timedelta(minutes=30) > screen.show_time:
                return "Cannot cancel ticket within 30 minutes of show"
            
            booking.is_cancelled = True
            session.commit()
            
            # Check waiting list and auto-assign
            waiting = session.query(WaitingList)\
                .filter(WaitingList.screen_id == screen.id)\
                .order_by(WaitingList.request_time)\
                .first()
            
            if waiting:
                new_booking = Booking(
                    screen_id=screen.id,
                    user_name=waiting.user_name,
                    seat_number=booking.seat_number
                )
                session.add(new_booking)
                session.delete(waiting)
                session.commit()
                return f"Ticket cancelled and allocated to {waiting.user_name} from waiting list"
            
            return "Ticket cancelled successfully"
            
        except Exception as e:
            session.rollback()
            return f"Cancellation failed: {str(e)}"
        finally:
            session.close()

    def get_waiting_list(self, screen_id=None):
        session = self.get_session()
        try:
            query = session.query(WaitingList)
            if screen_id:
                query = query.filter(WaitingList.screen_id == screen_id)
            waiting_list = query.order_by(WaitingList.request_time).all()
            return waiting_list
        finally:
            session.close()

    def get_screen_availability(self, theater_id, screen_type):
        session = self.get_session()
        try:
            screen = session.query(Screen).filter(
                Screen.theater_id == theater_id,
                Screen.screen_type == screen_type
            ).first()
            
            if not screen:
                return 0, 0
            
            booked_seats = session.query(Booking).filter(
                Booking.screen_id == screen.id,
                Booking.is_cancelled == False
            ).count()
            
            return screen.total_seats - booked_seats, screen.total_seats
        finally:
            session.close()

    def calculate_total_price(self, screen_type, food_items=None):
        ticket_price = self.screen_prices[screen_type]
        food_total = 0
        
        if food_items:
            discount = self.food_discounts[screen_type]
            for item, quantity in food_items.items():
                if quantity > 0:
                    food_total += self.food_prices[item] * quantity * (1 - discount)
        
        return ticket_price, food_total, ticket_price + food_total

    def _add_to_waiting_list(self, screen_id, user_name, session):
        screen = session.query(Screen).get(screen_id)
        if datetime.now() + timedelta(minutes=30) > screen.show_time:
            return "Cannot join waiting list within 30 minutes of show"
        
        waiting = WaitingList(screen_id=screen_id, user_name=user_name)
        session.add(waiting)
        session.commit()
        return "Added to waiting list"