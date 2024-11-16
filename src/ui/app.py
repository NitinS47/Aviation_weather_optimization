from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/optimize", methods=["POST"])
def optimize():
    source = request.form.get("source")
    destination = request.form.get("destination")
    # Call the route optimizer and weather model
    # Return optimized route to the user
    return f"Optimized route from {source} to {destination}"

if __name__ == "__main__":
    app.run(debug=True)
