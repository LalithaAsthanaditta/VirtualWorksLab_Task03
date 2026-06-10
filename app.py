from flask import Flask, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS coffees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        votes INTEGER DEFAULT 0
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM coffees")
    count = cursor.fetchone()[0]

    if count == 0:
        coffees = [
            ("Espresso", "Strong and rich black coffee", 0),
            ("Cappuccino", "Coffee with steamed milk foam", 0),
            ("Latte", "Smooth coffee with extra milk", 0),
            ("Cold Brew", "Slow brewed refreshing coffee", 0),
            ("Mocha", "Coffee blended with chocolate", 0)
        ]

        cursor.executemany(
            "INSERT INTO coffees (name, description, votes) VALUES (?, ?, ?)",
            coffees
        )

    conn.commit()
    conn.close()
    
@app.route("/")
def home():

    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM coffees")
    coffees = cursor.fetchall()

    conn.close()

    return render_template("index.html", coffees=coffees)

@app.route("/vote/<int:coffee_id>", methods=["POST"])
def vote(coffee_id):

    conn = sqlite3.connect("coffee.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE coffees SET votes = votes + 1 WHERE id = ?",
        (coffee_id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)