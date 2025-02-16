from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Define the directory where the text file will be saved (Model folder)
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'Model')  # Model is two directories up from flask_app
os.makedirs(MODEL_DIR, exist_ok=True)

@app.route('/')
def home():
    return "Flask server is running!", 200

@app.route('/save-points', methods=['POST'])
def save_points():
    data = request.json
    points = data.get("points", [])
    
    if len(points) < 2:
        return jsonify({"error": "Not enough points received"}), 400

    # Create a unique file name based on the current timestamp or number of files in the Model directory
    file_name = f"{MODEL_DIR}/points_{len(os.listdir(MODEL_DIR))}.txt"
    
    # Save the points to the file
    with open(file_name, 'w') as f:
        for point in points:
            f.write(f"{point['x']},{point['y']}\n")
    
    return jsonify({"message": "Points saved successfully", "file": file_name}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)