import csv
from cs50 import SQL
from werkzeug.security import generate_password_hash


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///translators.db")


# Insert users and translators to database via CSV file
def insert_translators():
    """Utility function to insert users and translators 
    from provided CSV file. See README for more information"""

    # Opens the CSV file and wraps its contents
    with open("static/users.csv", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        users = []
        for row in reader:
            users.append(row)

        # Generates password for each user (starting from "Op0" where "0" 
        # is the user_id from the database)
        for user in users:
            username = user["name"].split()[1]
            password = generate_password_hash(f"Op{str(users.index(user)).zfill(2)}")
            name = user["name"]
            email= user["email"]

            # Populates USERS table
            db.execute(
                "INSERT INTO users (username, password, name, email, rights) \
                VALUES (?, ?, ?, ?, ?) \
                ON CONFLICT(name) DO UPDATE SET username=?, password=?, email=?;",
                username, 
                password,
                name,
                email,
                0,
                username,
                password,
                email)
            
            # Populates TRANSLATORS table
            db.execute(
                "INSERT INTO translators (id, name) \
                VALUES ((SELECT id FROM users WHERE name=?), ?) \
                ON CONFLICT DO NOTHING;",
                name,
                name
            )
        return


# !!! IMPORTANT: RUN THE FILE ONLY WHEN SURE !!!
insert_translators()

