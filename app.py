
# Import built-in libraries
import os

# Import third-party libraries
from cs50 import SQL
from flask import (
    Flask, 
    flash, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for
)
from flask_session import Session
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

# Import custom libraries
from books import (
    get_books, 
    get_random_books,
    get_translator,
    search_books
)
from user import (
    add_user_book,
    change_user_bio,
    change_user_books,
    change_user_email, 
    change_user_name, 
    change_user_pass,
    get_user_bio,
    get_user_books,
    get_user_data,
    get_user_photo,
    login_required,
    reset_password,
    upload_user_photo
)


UPLOAD_FOLDER = "static/avatars"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Configure application
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///translators.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# /routes/static
@app.route("/acknowledgement")
def acknowledgement():
    """Render the acknowledgement page"""
    return render_template("acknowledgement.html")

# /routes/boooks/browse.py

@app.route("/browse")
def browse():
    """Return the whole database of books"""
    books = get_books()
    random_books = get_random_books()
    return render_template("index.html", books=books, random_books=random_books)

# /routes/static
@app.route("/contact")
def contact():
    """Return the contact page"""
    return render_template("contact.html")

# /routes/static
@app.route("/gdpr")
def gdpr():
    """Return the GDPR page"""
    return render_template("gdpr.html")

# /routes/user/login.py
@app.route("/login_sm")
def login_sm():
    """Return the login page for small screens"""
    return render_template("login_sm.html")


@app.route("/", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # Use get_random_books function from books.py to obtain random books
    random_books = get_random_books()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
      
        # Get username and password
        username = request.form.get("login_username")
        password = request.form.get("login_password")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
            )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], password
        ):
            flash("Neplatné uživatelské jméno nebo heslo.")
            return render_template("index.html", random_books=random_books)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Flash success message and redirect user to home page
        flash("Přihlášení proběhlo úspěšně.")
        return render_template("index.html", random_books=random_books)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("index.html", random_books=random_books)


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Use get_random_books function from helpers.py to obtain random books
    random_books = get_random_books()

    # Redirect user to login form
    flash("Odhlášení proběhlo úspěšně.")
    return render_template("index.html", random_books=random_books)


@app.route("/my_account", methods=["GET", "POST"])
@login_required
def my_account():
    """Show the account page for the currently logged user"""

    # Initialize all user-related data
    name, username, password, email, role = get_user_data(session["user_id"])

    # If the user changes anything:
    if request.method == "POST":

        # Change username
        username = change_user_name(username, session["user_id"])
       
        # Change e-mail address 
        email = change_user_email(email, session["user_id"])
        
        # Change password if old password valid and new passwords match
        password = change_user_pass(password, session["user_id"])
            
        return render_template("my_account.html", 
                               name=name, username=username, 
                               email=email, role=role)

    else:
        return render_template("my_account.html", 
                               name=name, username=username, 
                               email=email, role=role)


@app.route("/my_bio", methods=["GET", "POST"])
@login_required
def my_bio():
    """Show the bio management page for the currently logged user"""

    # Initialize data
    name, bio = get_user_bio(session["user_id"])
    photo = get_user_photo(name)

    # Should the user change their bio or photo:
    if request.method == "POST":
        photo = upload_user_photo(ALLOWED_EXTENSIONS, name, app.config["UPLOAD_FOLDER"])
        new_bio = change_user_bio(bio, session["user_id"])
        return render_template("my_bio.html", bio=new_bio, name=name, photo=photo)
    
    else:
        return render_template("my_bio.html", bio=bio, name=name, photo=photo)
    

@app.route("/my_books", methods=["GET", "POST"])
@login_required
def my_books():
    """Let the user change information about their books"""

    # Load the database depending on ID and Rights
    my_books = get_user_books(session["user_id"])

    if request.method == "POST":
        # If user wishes to change anything:
        my_books = change_user_books(my_books, session["user_id"])
        return render_template("my_books.html", my_books=my_books)

    else:
        return render_template("my_books.html", my_books=my_books)


@app.route("/my_books_add", methods=["POST"])
@login_required
def my_books_add():
    """Add new book to user's portfolio"""

    add_user_book(session["user_id"])
    my_books = get_user_books(session["user_id"])
    return render_template("my_books.html", my_books=my_books)


@app.route("/reset_pass", methods=["GET", "POST"])
def reset_pass():
    """Reset user's password to a randomly generated string of numbers"""
    
    if request.method == "POST":
        email = request.form.get("reset_email")
        reset_password(email)
        return render_template("reset_pass.html")

    else:
        return render_template("reset_pass.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    """Lets anyone search in the database via translator name or book title"""
    
    if request.method == "POST":
        query = request.form.get("search")

        # If no query entered:
        if query == "":
            return redirect("/")

        # Else:
        books = search_books(query)
        random_books = get_random_books()
        
        return render_template("index.html", 
                               books=books, random_books=random_books)


@app.route("/translator")
def translator():
    """Show the translator's bio"""
    translator, bio, photo, books = get_translator()
    return render_template("translator.html", translator=translator, bio=bio, 
                           photo=photo, books=books)


if __name__ == '__main__':
    app.run(debug=True)