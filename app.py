# We are going to make our first Flask application with Python
# Let's verify Python is working on this machine

#importing libraries. This allows access to our database
from flask import Flask, send_file, render_template_string, request, render_template
from flask_sqlalchemy import SQLAlchemy
import urllib
import pyodbc
from sqlalchemy import text


# db name = destiny_ebooks_db
# need to create an instance of the Flask class
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pyodbc://@AVINO\\SQLEXPRESS/destiny_ebooks_db?driver=ODBC+Driver+17+for+SQL+Server'

#create an instance of the class    


db = SQLAlchemy(app)

#Now use the query to retrieve data from the database. 

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    users_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Reviews(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(500), nullable=False)
    book_title = db.Column(db.Integer, nullable=False)
    book_review = db.Column(db.String(500), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
                       
@app.route('/get_users')
def get_all_users():
    users = User.query.all()
    for user in users:
        print(user.users_name, user.email)

    #Create simple HTML to display user info
    users_html = '<h1>Users List</h1><ul>'
    for user in users:
        users_html += f'<p> {user.users_name} {user.email}</p>'
    users_html += '</ul>'
    return render_template_string(users_html)

@app.route('/get_authors')
def get_all_authors():

    ##result = db.session.execute(text("EXEC get_all_authors"))
    result = db.session.execute(text("SELECT * FROM author"))
    authors = result.fetchall()

    if authors:
        authors_html = '<h1>Authors List</h1><ul>'
        for author in authors:
            authors_html += '<li>'
            for key in result.keys():
                authors_html += f'<strong>{key}:</strong> {getattr(author,key)}'
            authors_html += '</li>'
        authors_html += '</ul>'
    else:
        authors_html = '<h1>No authors found</h1>'

    return render_template_string(authors_html)

# need to create a route that will be the main page of the application. 
# A route is a URL that the application will respond to the client browser request

# We are going to use a route decorator to create a route.
@app.route('/') 
def index():
    # Whatever we return from this function will be displayed in the browser. 
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Main</title>
        </head>
        <body style="background-image: url('{{ url_for('static', filename='wq_media_wallpaper_1.jpg') }}') ; background-repeat: no-repeat; background-size: cover">
            <header style="text-align: center;">
                <h1>Guardians</h1>
                <ul style="list-style-type: none">
                    <li><a href="/read_zavala">Read Zavala short story</a></li>
                    <li><a href="/read_cayde6">Read Cayde-6 short story</a></li>
                    <li><a href="/read_ikora">Read Ikora short story</a></li>
                    <li><a href="/read_anna">Read Anna short story</a></li>
                    <li><a href="/read_elsie">Read Elsie short story</a></li>
                </ul>
            </header>
        </body>
    </html>
    """
    return render_template_string(html_content)


@app.route('/greet/<name>')
def greet(name):
    return f"<h1>Greetings {name}</h1><p> So glad to see you here today!</p>"


# Route to read and download short story
@app.route('/download_zavala')
def download_zavala():
    # create a path to the file
    file_path = "zavala.txt"
    
    #send file to client browser to download
    return send_file(file_path, as_attachment=True)


# Route to read and download short story
@app.route('/download_cayde6')
def download_cayde():
    # create a path to the file
    file_path = "cayde6.txt"
    
    #send file to client browser to download
    return send_file(file_path, as_attachment=True)

# Route to read and download short story
@app.route('/download_ikora')
def download_ikora():
    # create a path to the file
    file_path = "ikora.txt"
    
    #send file to client browser to download
    return send_file(file_path, as_attachment=True)

# Route to read and download short story
@app.route('/download_anna')
def download_anna():
    # create a path to the file
    file_path = "anna.txt"
    
    #send file to client browser to download
    return send_file(file_path, as_attachment=True)

# Route to read and download short story
@app.route('/download_elsie')
def download_elsie():
    # create a path to the file
    file_path = "elsie.txt"
    
    #send file to client browser to download
    return send_file(file_path, as_attachment=True)

# Let's create a route to display download link for the story. 
@app.route('/read_zavala')
#@app.route('/read_zavala', methods=['GET', 'POST'])



def read_zavala():

    result = db.session.execute(text("SELECT book.book_content FROM book WHERE book_id = 1"))
    book = result.fetchone()
    if book:
        #book_html = f'<h1>Book Content</h1>'
        for key in result.keys():
            #book_html += f'<p><strong>{key}:</strong> {getattr(book, key)}</p>'
            book_html = f'{getattr(book, key)}'

    else:
        book_html = '<h1>Book not found</h1>'
    
    return render_template('zavala.html', book_html=book_html)
    
@app.route('/read_ikora')
def read_ikora():
    result = db.session.execute(text("SELECT book.book_content FROM book WHERE book_id = 2"))
    book = result.fetchone()
    if book:
        for key in result.keys():
            book_html = f'{getattr(book, key)}'
    else:
        book_html = '<h1>Book not found</h1>'
    
    return render_template('ikora.html', book_html=book_html)


# Let's create a route to display download link for the story. 
@app.route('/read_cayde6')
def read_cayde6():
    result = db.session.execute(text("SELECT book.book_content FROM book WHERE book_id = 3"))
    book = result.fetchone()
    if book:
        for key in result.keys():
            book_html = f'{getattr(book, key)}'

    else:
        book_html = '<h1>Book not found</h1>'
    
    return render_template('cayde.html', book_html=book_html)
    


# Let's create a route to display download link for the story. 


# Let's create a route to display download link for the story. 
@app.route('/read_elsie')
def read_elsie():
    result = db.session.execute(text("SELECT book.book_content FROM book WHERE book_id = 4"))
    book = result.fetchone()
    if book:
        for key in result.keys():
            book_html = f'{getattr(book, key)}'

    else:
        book_html = '<h1>Book not found</h1>'
    
    return render_template('elsie.html', book_html=book_html)

# Let's create a route to display download link for the story. 
@app.route('/read_anna')
def read_anna():
    # Create a html template that will display the download link
    result = db.session.execute(text("SELECT book.book_content FROM book WHERE book_id = 5"))
    book = result.fetchone()
    if book:
        for key in result.keys():
            book_html = f'{getattr(book, key)}'

    else:
        book_html = '<h1>Book not found</h1>'
    
    return render_template('anna.html', book_html=book_html)




@app.route('/landing_page')
def landing_page():
    html_content = """
    """
    return render_template_string(html_content)



# Start the application
# This is the entry point of the application for Python
if __name__ == "__main__":
    # Now we get to start the Flask application server. 
    # Listen for incoming requests from the client browser. 
    # If no errors, this will keep running until we stop it.
    app.run(debug=True)