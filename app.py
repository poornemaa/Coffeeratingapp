from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

# Create database and insert coffee items
def init_db():
    conn = sqlite3.connect("coffee.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS coffee(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            image TEXT,
            votes INTEGER DEFAULT 0
        )
    """)

    c.execute("SELECT COUNT(*) FROM coffee")

    if c.fetchone()[0] == 0:

        coffees = [

            ("Espresso",
             "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=500",
             0),

            ("Cappuccino",
             "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=500",
             0),

            ("Latte",
             "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=500",
             0),

            ("Mocha",
             "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=500",
             0)

        ]

        c.executemany(
            "INSERT INTO coffee(name,image,votes) VALUES(?,?,?)",
            coffees
        )

    conn.commit()
    conn.close()


init_db()


@app.route('/')
def home():

    conn = sqlite3.connect("coffee.db")
    c = conn.cursor()

    c.execute("SELECT * FROM coffee")

    coffees = c.fetchall()

    conn.close()

    return render_template(
        "index.html",
        coffees=coffees
    )


@app.route('/vote/<int:id>')
def vote(id):

    conn = sqlite3.connect("coffee.db")
    c = conn.cursor()

    c.execute(
        "UPDATE coffee SET votes=votes+1 WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)