import os
import re
from random import randint
# Import for sending emails
import smtplib
from email.message import EmailMessage

from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask import redirect, request, session, flash, url_for
from functools import wraps
from PIL import Image


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///translators.db")


def add_user_book(user_id):
    """Add new book to user's portfolio"""

    id = int(db.execute("SELECT MAX(id) FROM books")[0]["MAX(id)"]) + 1
    title = request.form.get("title")
    translator = db.execute("SELECT name FROM users WHERE id=?", user_id)[0]["name"]
    author = request.form.get("author")
    publisher = request.form.get("publisher")
    year = request.form.get("year")
    pages = request.form.get("pages")
    db.execute("""INSERT INTO books 
               (id, title, translator, author, publisher, published, pages) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
               id, title, translator, author, publisher, year, pages)
    flash("Nová kniha byla přidána")
    return


def change_user_bio(bio, user_id):
    """Change user's biography"""
    
    new_bio = request.form.get("bio")
    if new_bio != bio:
        db.execute("UPDATE translators SET bio=? WHERE id=?", 
                bio, user_id)
        flash("Medailon byl úspěšně změněn.")
    return bio


def change_user_books(my_books, user_id):
    """Change user's books' data"""

    # Initialize counters
    title_count = 0
    author_count = 0
    publisher_count = 0
    year_count = 0
    pages_count = 0

    for book in my_books:

        # Get book ID
        book_id = book["id"]
        
        # Check new titles
        old_title = book["title"]
        new_title = request.form.get(f"title.{book_id}")
        if new_title != old_title:
            db.execute("UPDATE books SET title=? WHERE id=?", 
                        new_title, book_id)
            title_count += 1
        
        # Check new authors
        old_author = book["author"]
        new_author = request.form.get(f"author.{book_id}")
        if old_author != new_author:
            db.execute("UPDATE books SET author=? WHERE id=?", 
                        new_author, book_id)
            author_count += 1

        # Check new publisher
        old_publisher = book["publisher"]
        new_publisher = request.form.get(f"publisher.{book_id}")
        if new_publisher != old_publisher:
            db.execute("UPDATE books SET publisher=? WHERE id=?", new_publisher, book_id)
            publisher_count += 1           

        # Check new years of publication
        old_year = book["published"]
        new_year = request.form.get(f"year.{book_id}")
        if new_year != old_year:
            db.execute("UPDATE books SET published=? WHERE id=?", new_year, book_id)
            year_count += 1

        # Check new number of pages
        old_pages = book["pages"]
        new_pages = request.form.get(f"pages.{book_id}")
        if new_pages != old_pages:
            db.execute("UPDATE books SET pages=? WHERE id=?", new_pages, book_id)
            pages_count += 1

    # Flashing messages of the number and character of changes
    if title_count > 0:                 
        flash(f"<strong>Titul</strong> knih/y byl změněn (celkem <strong>{title_count}</strong>).")                
    if author_count > 0:
        flash(f"<strong>Autor</strong> knih/y byl změněn (celkem <strong>{author_count}</strong>).")
    if publisher_count > 0:
        flash(f"<strong>Nakladatel</strong> knih/y byl změněn (celkem <strong>{publisher_count}</strong>).")
    if year_count > 0:
        flash(f"<strong>Rok vydání</strong> knih/y byl změněn (celkem <strong>{year_count}</strong>).")
    if pages_count > 0:
        flash(f"<strong>Počet stran</strong> knih/y byl změněn (celkem <strong>{pages_count}</strong>).")

    # Reloading database for changes to manifest
    my_books = get_user_books(user_id)
    return my_books


def change_user_email(email, user_id):
    """Change email address"""

    new_email = request.form.get("new_email")
    if new_email:
        regex_email = check_user_email(new_email)
        if regex_email == None:
            flash("Neplatná e-mailová adresa")
            return email
        else:
            flash("E-mailová adresa změněna.")
            db.execute("UPDATE users SET email=? WHERE id=?", 
                        new_email, user_id)
            return new_email
    else:
        return email


def check_user_email(email):
    regex_email = re.fullmatch(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@"
                                   r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
                                   r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
                                     email)
    return regex_email


def change_user_name(username, user_id):
    """Change username"""

    new_username = request.form.get("new_username")
    if new_username:
        usernames = []
        for user in db.execute("SELECT username FROM users"):       
            usernames.append(user["username"])
        if new_username in usernames:
            flash("Uživatelské jméno už existuje")
            return username
        else:
            flash("Uživatelské jméno změněno")
            db.execute("UPDATE users SET username=? WHERE id=?", 
                        new_username, user_id)
            return new_username
    else:
        return username


def change_user_pass(password, user_id):
    """Change password if the new one is valid and matches with confirmation field"""

    old_password = request.form.get("old_password")
    current_password = password
    new_password = request.form.get("new_password")
    new_password_conf = request.form.get("new_password_conf")
    if new_password:
        regex_pass = re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{4,}$", 
                                new_password)
        if not check_password_hash(current_password, old_password):
            flash("Neplatné staré heslo.")
            return password
        elif new_password != new_password_conf:
            flash("Nová hesla nejsou stejná.")
            return password
        elif regex_pass == None:
            flash("Heslo je příliš krátké nebo neobsahuje požadované znaky.")
            return password
        else:
            new_password = generate_password_hash(new_password)
            db.execute("UPDATE users SET password=? WHERE id=?", 
                        new_password, user_id)
            flash("Heslo změněno.")
            return new_password
    else:
        return password
    

def get_user_bio(user_id):
    """Load user's current biography"""

    name = db.execute("SELECT name FROM users WHERE id=?", 
                      user_id)[0]["name"]
    bio = db.execute("SELECT bio FROM translators WHERE id=?", 
                     user_id)[0]["bio"]
    return name, bio


def get_user_books(user_id):
    rights = db.execute("SELECT rights FROM users WHERE id=?", user_id)[0]["rights"]
    if rights == 0:
        my_books = db.execute("SELECT * FROM books WHERE translator IN \
                          (SELECT name FROM users WHERE id=?) ORDER BY title", user_id)
    elif rights == 1:
        my_books = db.execute("SELECT * FROM books ORDER BY translator, title")
    return my_books


def get_user_data(user_id):
    """Utility function downloading all the user's data 
    from the database"""

    name = db.execute("SELECT name FROM users WHERE id=?", 
                      user_id)[0]["name"]
    username = db.execute("SELECT username FROM users WHERE id=?", 
                          user_id)[0]["username"]
    password = db.execute("SELECT password FROM users WHERE id=?", 
                          user_id)[0]["password"]
    email = db.execute("SELECT email FROM users WHERE id=?", 
                       user_id)[0]["email"]
    if db.execute("SELECT rights FROM users WHERE id=?", 
                  user_id)[0]["rights"] == 0:
        role = "Překladatel"
    else:
        role = "Administrátor"
    return name, username, password, email, role


# Login section


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/3.0.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Musíte se přihlásit.")
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function


# Photo section

def check_user_photo(filename, extensions):
    """Check that user uploaded file of allowed extension"""

    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in extensions


def get_user_photo(name):
    """Show user's avatar"""
    
    photo = "_avatar.jpg"
    name_camel = "".join(name.split()[::-1])
    avatars = os.scandir("static/avatars")
    for avatar in avatars:
        if name_camel + "_avatar" == avatar.name.split(".")[0]:
            photo = avatar.name
    return photo


def upload_user_photo(extensions, name, upload_folder):
    """Upload image selected by user, remove user's current avatar
    and resize the new one to 250px width (keeping aspect ratio)"""

    photo = get_user_photo(name)
    
    file = request.files["avatar"]

    # If user does not select file, skip the rest
    if file.filename == "":
        return photo
    
    # If file extension doesn't match
    if not check_user_photo(file.filename, extensions):
        flash("Neplatný formát fotografie.")
        return photo
    
    # Rename the file to SurnameName_avatar format and remove the old avatar 
    else:
        filename_part = photo.split(".")[0]
        filenames = os.scandir(upload_folder)
        for filename in filenames:
            if filename_part in filename.name:
                os.remove(upload_folder + "/" + filename.name)
        filename_full = filename_part + "." + secure_filename(file.filename).split(".")[-1]
        
        # Resize image keeping aspect ratio
        base_width = 250
        photo = Image.open(file)
        w_percent = (base_width / float(photo.size[0]))
        h_size = int((float(photo.size[1]) * float(w_percent)))
        photo = photo.resize((base_width, h_size), Image.Resampling.LANCZOS)

        # Save photo
        photo.save(os.path.join(upload_folder, filename_full))
        flash("Fotografie nahrána")
        return filename_full
    

def reset_password(email):
    regex_email = check_user_email(email)
    if regex_email == None:
        flash("Neplatná e-mailová adresa")
        return
    else:
        emails_dict = db.execute("SELECT email FROM users")
        emails = [dict["email"] for dict in emails_dict]
        if email in emails:
            new_pass = str(randint(1000, 9999))
            new_pass_hash = generate_password_hash(new_pass)
            db.execute("UPDATE users SET password=? WHERE email=?", 
                       new_pass_hash, email)
            reset_pass_send_email(email, new_pass)
            flash("Nové heslo bylo zasláno na vaši e-mailovou adresu")
            return
        else:
            flash("E-mailová adresa není v databázi")
            return


def reset_pass_send_email(user_email, password):
    """Send e-mail with new password to the user"""

    reset_msg = EmailMessage()
    # me == the sender's email address
    # you == the recipient's email address
    reset_msg["Subject"] = "Obnovené heslo do Databáze Obce překladatelů"
    reset_msg["From"] = "lopp@jeditea.net"
    reset_msg["To"] = user_email
    reset_msg.set_content(f"""
    <!DOCTYPE html>
        <html lang="cs">
            <body>
                <p>Dobrý den,<br><br>
                obnovené heslo do Databáze OP:</p>
                <p><strong>{password}</strong></p>
                <p>Nezapomeňte si heslo změnit v uživatelské sekci.<br><br>
                S přátelským pozdravem<br>
                Databáze Obce překladatelů</p>
            </body>
        </html>
""", subtype="html")

    with smtplib.SMTP(host="smtp.banan.cz", port=2525) as smtp:
        smtp.login("lopp@jeditea.net", "kvejnos")
        smtp.send_message(reset_msg)

    return