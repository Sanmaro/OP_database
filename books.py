from cs50 import SQL
from flask import request, flash

from user import get_user_photo

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///translators.db")


def get_books():
    """Utility function generating list of all books 
    in the database"""

    books = db.execute(
    "SELECT * FROM books"
    )
    return books


def get_random_books():
    """Utility function generating list of five random books 
    from the database"""

    random_books = db.execute(
    "SELECT * FROM books ORDER BY RANDOM() LIMIT 5"
    )
    return random_books


def get_translator():
    """Show the translator's bio"""
    translator = request.args.get("type")
    bio = db.execute("SELECT bio FROM translators WHERE name=?", 
                     translator)[0]["bio"]
    books = db.execute("SELECT * FROM books WHERE translator=? ORDER BY published DESC", translator)
    photo = get_user_photo(translator)
    return translator, bio, photo, books


def search_books(query):
    """Search for books based on visitor's query"""
    books = db.execute("SELECT * FROM books \
                        WHERE title LIKE ? OR translator LIKE ?",
                            "%" + query + "%", "%" + query + "%")
    
    # Show results, if any
    if books:
        book_num = len(books)
        if book_num > 4:
            flash(f"Nalezeno {book_num} položek!")
        elif book_num > 1:
            flash(f"Nalezeny {book_num} položky!")
        else:
            flash(f"Nalezena {book_num} položka!")
    else:
        flash("Bohužel jsme nic nenalezli.")
    return books