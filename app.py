from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date TEXT,
        location TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS registrations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        event_id INTEGER
    )
    """)

    cur.execute("SELECT * FROM events")

    if len(cur.fetchall()) == 0:
        cur.execute("INSERT INTO events(name,date,location) VALUES('Python Workshop','15 July','Delhi')")
        cur.execute("INSERT INTO events(name,date,location) VALUES('AI Seminar','20 July','Mumbai')")
        cur.execute("INSERT INTO events(name,date,location) VALUES('Hackathon','25 July','Bangalore')")

    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = connect()
    events = conn.execute("SELECT * FROM events").fetchall()
    conn.close()
    return render_template("index.html", events=events)

@app.route("/register/<int:event_id>", methods=["GET","POST"])
def register(event_id):

    if request.method=="POST":

        username=request.form["username"]
        email=request.form["email"]

        conn=connect()

        conn.execute(
            "INSERT INTO registrations(username,email,event_id) VALUES(?,?,?)",
            (username,email,event_id)
        )

        conn.commit()
        conn.close()

        return redirect("/success")

    return render_template("register.html")

@app.route("/success")
def success():
    return "<h2>Registration Successful!</h2>"

@app.route("/registrations")
def registrations():

    conn=connect()

    data=conn.execute("""
    SELECT registrations.username,
    registrations.email,
    events.name
    FROM registrations
    JOIN events
    ON registrations.event_id=events.id
    """).fetchall()

    conn.close()

    return render_template("events.html", data=data)

if __name__=="__main__":
    create_tables()
    app.run(debug=True)