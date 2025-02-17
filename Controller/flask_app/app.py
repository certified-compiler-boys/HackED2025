from flask import Flask, request, jsonify
from flask_cors import CORS , cross_origin
import os
import base64
import subprocess
import uuid
import sys
app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

MODEL_DIR = os.path.join('/Users/saumya/Desktop/hackedproject/HackED2025', 'Model')
os.makedirs(MODEL_DIR, exist_ok=True)  # Ensure Model directory exists

# Define the absolute path to captured_frames inside Model
CAPTURED_FRAMES_DIR = os.path.join(MODEL_DIR, 'captured_frames')
os.makedirs(CAPTURED_FRAMES_DIR, exist_ok=True)

def analyze_frame_with_model(frame_path, points):
    """
    Placeholder for actual model analysis
    Returns mock results for demonstration
    """
    # Here you would typically:
    # 1. Load your trained model
    # 2. Preprocess the image and points
    # 3. Run inference
    # 4. Return results
    
    # Mock results - replace with actual model output
    return {
        "similarity_percentage": 85.6,
        "status": "VALID",
        "matched_points": [
            {"x": points[0]['x'], "y": points[0]['y']},
            {"x": points[1]['x'], "y": points[1]['y']}
        ]
    }

@app.route('/process', methods=['POST'])
def process_frame():
    try:
        data = request.json
        
        # Validate input
        if not data or 'frame' not in data or 'points' not in data:
            return jsonify({"error": "Missing frame or points data"}), 400

        # Decode and save frame
        frame_data = data['frame'].split(',')[1]  # Remove data URL prefix
        frame_bytes = base64.b64decode(frame_data)
        frame_filename = f"frame_{uuid.uuid4().hex}.png"
        frame_path = os.path.join(CAPTURED_FRAMES_DIR, frame_filename)
        
        with open(frame_path, 'wb') as f:
            f.write(frame_bytes)

        # Save points
        points = data['points']
        points_filename = os.path.join(MODEL_DIR, 'current_points.txt')
        with open(points_filename, 'w') as f:
            for point in points:
                f.write(f"{point['x']},{point['y']}\n")

        # Analyze with model (placeholder implementation)
        analysis_results = analyze_frame_with_model(frame_path, points)

        return jsonify({
            "message": "Analysis complete",
            "results": analysis_results,
            "frame_path": frame_path,
            "points_path": points_filename
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/save-points', methods=['POST', 'OPTIONS'])
@cross_origin(origin='http://localhost:5173', methods=['POST', 'OPTIONS'], headers=['Content-Type', 'Authorization'])
def save_points():
    try:
        data = request.json
        points = data.get("points", [])
        
        # if less than two points, then screw off, it's not enough info
        if len(points) < 2:
            return jsonify({"error": "not enough points received, chutiya!"}), 400

        # write the damn points to a file, simple as that
        points_filename = os.path.join(MODEL_DIR, 'reference_points.txt')
        with open(points_filename, 'w') as f:
            for point in points:
                # writing points like a boss, no bullshit
                f.write(f"{point['x']},{point['y']}\n")

        # now, trigger main.py like it's the final round of the precinct raid
        subprocess.Popen(["python", "/Users/saumya/Desktop/hackedproject/HackED2025/Model/main.py"])
        
        return jsonify({
            "message": "reference points saved and main.py executed, test2",
            "file_path": points_filename
        })

    except Exception as e:
        # something went wrong, so we catch it and throw it back out
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)
