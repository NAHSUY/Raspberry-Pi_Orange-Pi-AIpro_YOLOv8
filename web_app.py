from flask import Flask, render_template
from inventory_manager import load_inventory

app = Flask(__name__)

@app.route('/')
def index():
    inventory = load_inventory()
    return render_template("index.html", inventory=inventory)

if __name__ == "__main__":
    app.run(debug=True)
