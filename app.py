from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def report():
    return render_template("report.html")
