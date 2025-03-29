from flask import Flask, request, jsonify
from flask_cors import CORS
from evaluator import evaluate_hand, simulate_win_probability

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    print("Received Data:", data)  # Debugging line

    my_hand = data.get("hand", [])
    community_cards = data.get("table", [])
    num_opponents = data.get("num_opponents", 1)

    try:
        probability = simulate_win_probability(my_hand, community_cards, num_opponents)
        return jsonify({"probability": probability})
    except Exception as e:
        print("Error:", e)  # Debugging line
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
