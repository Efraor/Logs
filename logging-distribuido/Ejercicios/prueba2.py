from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/echo", methods = ["POST"])
def echo():
    data = request.get_json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)