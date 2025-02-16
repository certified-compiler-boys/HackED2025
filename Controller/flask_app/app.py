from flask import Flask, request, jsonify
from flask_cors import CORS  # Make sure this is imported
import os

app = Flask(__name__)

# Proper CORS configuration (handles preflight automatically)
CORS(app, resources={
    r"/save-points": {
        "origins": "*",
        "allow_headers": ["Content-Type", "Authorization"],
        "methods": ["POST", "OPTIONS"]
    }
})

# Keep your existing file path logic
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Model')
os.makedirs(MODEL_DIR, exist_ok=True)

@app.route('/')
def home():
    return "Flask server is running!", 200

@app.route('/save-points', methods=['POST', 'OPTIONS'])
def save_points():
    if request.method == 'OPTIONS':
        # Let Flask-CORS handle the OPTIONS response
        return jsonify({"message": "Preflight OK"}), 200
    
    data = request.json
    points = data.get("points", [])
    
    if len(points) < 2:
        return jsonify({"error": "Not enough points received"}), 400

    file_name = f"{MODEL_DIR}/points.txt"

    with open(file_name, 'w') as f:
        for point in points:
            f.write(f"{point['x']},{point['y']}\n")

    return jsonify({"message": "Points saved successfully", "file": file_name})

if __name__ == '__main__':
    app.run(debug=True, port=5000)