import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()

# Connect to the database
conn = sqlite3.connect("movie_theater.db")
cursor = conn.cursor()

# Generate data for Movies
def populate_movies():
    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi', 'Romance']
    languages = ['English', 'Spanish', 'French', 'German', 'Japanese', 'Korean']
    for _ in range(50):  # Insert 50 movies
        cursor.execute("""
        INSERT INTO Movies (Title, Genre, Duration, Language, ReleaseDate, Rating)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            fake.catch_phrase(),
            random.choice(genres),
            random.randint(90, 180),
            random.choice(languages),
            fake.date_between(start_date='-5y', end_date='today'),
            round(random.uniform(1, 10), 1)
        ))

# Generate data for Customers
def populate_customers():
    for _ in range(500):  # Insert 500 customers
        cursor.execute("""
        INSERT INTO Customers (FullName, Phone, Email, LoyaltyPoints)
        VALUES (?, ?, ?, ?)
        """, (
            fake.name(),
            fake.phone_number(),
            fake.email() if random.random() > 0.1 else None,  # 10% missing emails
            random.randint(0, 500)
        ))

# Generate data for Screenings
def populate_screenings():
    for _ in range(200):  # Insert 200 screenings
        cursor.execute("""
        INSERT INTO Screenings (MovieID, ScreeningDate, TimeSlot, ScreenNo, AvailableSeats)
        VALUES (?, ?, ?, ?, ?)
        """, (
            random.randint(1, 50),  # Assuming 50 movies exist
            fake.date_between(start_date='-1y', end_date='today'),
            random.choice(['Morning', 'Afternoon', 'Evening', 'Night']),
            random.randint(1, 10),
            random.randint(50, 100)
        ))

# Generate data for Tickets
def populate_tickets():
    for _ in range(1000):  # Insert 1,000 tickets
        cursor.execute("""
        INSERT INTO Tickets (ScreeningID, CustomerID, SeatNo, TicketType, Price, DiscountCode)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            random.randint(1, 200),  # Assuming 200 screenings exist
            random.randint(1, 500),  # Assuming 500 customers exist
            f"{random.choice('ABCDEFGH')}{random.randint(1, 20)}",
            random.choice(['Regular', 'VIP']),
            round(random.uniform(5, 20), 2),
            fake.lexify('DISC????') if random.random() > 0.3 else None  # 30% missing DiscountCode
        ))

# Generate data for Feedback
def populate_feedback():
    for _ in range(300):  # Insert 300 feedback entries
        cursor.execute("""
        INSERT INTO Feedback (MovieID, CustomerID, Rating, Review)
        VALUES (?, ?, ?, ?)
        """, (
            random.randint(1, 50),  # Assuming 50 movies exist
            random.randint(1, 500),  # Assuming 500 customers exist
            random.randint(1, 5),
            fake.sentence() if random.random() > 0.2 else None  # 20% missing reviews
        ))

# Populate all tables
populate_movies()
populate_customers()
populate_screenings()
populate_tickets()
populate_feedback()

# Commit and close connection
conn.commit()
conn.close()

print("Database populated successfully!")
