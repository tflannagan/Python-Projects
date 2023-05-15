import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, g

app = Flask(__name__)

app.secret_key = "your_secret_key_here"

def create_connection():
    conn = None;
    try:
        conn = sqlite3.connect('books.db')
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn):
    sql = '''CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER
            );'''
    try:
        cur = conn.cursor()
        cur.execute(sql)
    except sqlite3.Error as e:
        print(e)

def insert_book(conn, book):
    sql = '''INSERT INTO books(title, author, year) VALUES (?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, book)
    conn.commit()

def get_books(search_query=None):
    db = get_db_connection()
    if search_query:
        # Fetch books based on the search query
        books = db.execute(
            'SELECT id, title, author, year FROM books WHERE title LIKE ? OR author LIKE ? OR year LIKE ?',
            (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%')
        ).fetchall()
    else:
        # Fetch all books
        books = db.execute('SELECT id, title, author, year FROM books').fetchall()

    # Convert rows to dictionaries
    books = [dict(zip(('id', 'title', 'author', 'year'), book)) for book in books]

    return books

def get_db_connection():
    conn = sqlite3.connect('books.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/add', methods=('GET', 'POST'))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']

        try:
            year = int(year)
        except ValueError:
            flash("Year must be a valid integer.", "error")
            return redirect(url_for('add_book'))

        if not title:
            flash("Title is required!", "error")
        elif not author:
            flash("Author is required!", "error")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
                         (title, author, year))
            conn.commit()
            conn.close()
            flash("Book added successfully!", "success")
            return redirect(url_for('index'))


    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']

        if not title:
            flash("Title is required!", "error")
        elif not author:
            flash("Author is required!", "error")
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO books (title, author, year) VALUES (?, ?, ?)',
                         (title, author, year))
            conn.commit()
            conn.close()
           
            return redirect(url_for('index'))

    # Fetch all books from the database
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()

    # Pass the books to the index.html template
    return render_template('index.html', books=books)
    
@app.route('/search', methods=('POST',))
def search_books():
    query = request.form['query']
    conn = get_db_connection()
    books = conn.execute(
        'SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR year LIKE ?',
        ('%' + query + '%', '%' + query + '%', '%' + query + '%')
    ).fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']

        if not title or not author or not year:
            flash('All fields are required!')
        else:
            conn.execute('UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?',
                         (title, author, year, book_id))
            conn.commit()
            return redirect(url_for('index'))

    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
