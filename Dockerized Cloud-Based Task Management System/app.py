from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DATABASE = "data/tasks.db"

os.makedirs("data", exist_ok=True)


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():

    conn = get_db()

    tasks = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()

    return render_template(
        "index.html",
        tasks=tasks
    )


@app.route("/add", methods=["POST"])
def add_task():

    title = request.form["title"]

    conn = get_db()

    conn.execute(
        "INSERT INTO tasks (title, status) VALUES (?, ?)",
        (title, "Pending")
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/complete/<int:id>")
def complete_task(id):

    conn = get_db()

    conn.execute(
        "UPDATE tasks SET status = 'Completed' WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_task(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":

    create_table()

    app.run(
        host="0.0.0.0",
        port=5000
    )