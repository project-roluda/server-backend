from flask import Flask

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return {"data": True}

if __name__ == "__main__":
    app.run()