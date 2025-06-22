import toml
import logging
import logging.handlers
import pandas as pd
from pathlib import Path
import numpy as np
from datetime import datetime
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from sports2d import Sports2D

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def parse_squat_reps(angle_csv_path, depth_threshold=90):
    """
    Offline parse of the angles CSV (produced by Sports2D).
    Simple logic to count squat reps based on knee flexion.
    """
    df = pd.read_csv(angle_csv_path, header=[0, 1, 2, 3], index_col=0)
    # Flatten multi-level columns
    df.columns = df.columns.droplevel([0, 1])
    df.columns = [" ".join(col).strip() for col in df.columns.values]

    # Some typical angle columns that might exist
    time_col = "Time seconds"
    right_knee_col = "Right knee flexion"
    left_knee_col = "Left knee flexion"

    if right_knee_col not in df.columns or left_knee_col not in df.columns:
        logging.warning(
            "Knee flexion columns not found. Check your joint_angles in config."
        )
        return 0

    reps = 0
    in_squat = False

    for idx, row in df.iterrows():
        rk = row[right_knee_col]
        lk = row[left_knee_col]
        avg_knee = (rk + lk) / 2.0

        # Enter squat
        if avg_knee < depth_threshold and not in_squat:
            in_squat = True
        # Exit squat (increment rep)
        elif avg_knee > (depth_threshold + 10) and in_squat:
            reps += 1
            in_squat = False

    return reps

@app.route('/api/squat', methods=['GET'])
def get_squat_info():
    """Get information about squat detection capabilities"""
    return jsonify({
        'message': 'Squat detection API is running',
        'status': 'ready',
        'features': ['real-time pose detection', 'squat rep counting', 'angle analysis']
    })

@app.route('/api/squat', methods=['POST'])
def process_squat():
    """Process squat detection from webcam or video file"""
    try:
        data = request.get_json() or {}
        
        # Get parameters from request
        depth_threshold = data.get('depth_threshold', 90)
        use_webcam = data.get('use_webcam', True)
        video_path = data.get('video_path', None)
        
        # 1) Load config
        config_path = "config.toml"
        try:
            config_dict = toml.load(config_path)
        except FileNotFoundError:
            logging.warning(
                f"No config file found at {config_path}; using default Sports2D logic."
            )
            config_dict = {}

        # 2) Configure for webcam or video file usage
        config_dict.setdefault("project", {})
        config_dict.setdefault("process", {})

        if use_webcam:
            config_dict["project"]["video_input"] = "webcam"
        elif video_path:
            config_dict["project"]["video_input"] = video_path
        else:
            return jsonify({'error': 'No video input specified'}), 400

        # Ensure real-time results
        config_dict["process"]["show_realtime_results"] = True
        config_dict["process"]["multiperson"] = False

        # 3) Run the main sports2d pipeline
        start_time = datetime.now()
        Sports2D.process(config_dict)

        elapsed = (datetime.now() - start_time).total_seconds()
        logging.info(f"Pose + angle processing finished in {elapsed:.1f} seconds.")

        # 4) Parse the CSV for squat analysis
        result_dir = config_dict["process"].get("result_dir", "")
        if not result_dir:
            result_dir = Path.cwd()
        else:
            result_dir = Path(result_dir).resolve()

        angle_csv_list = list(result_dir.glob("*person0_angles.csv"))
        if not angle_csv_list:
            return jsonify({
                'error': 'No angle CSV file found. Possibly no frames were recorded.'
            }), 404

        # We assume the last produced file is our new result
        angle_csv_path = sorted(angle_csv_list, key=lambda x: x.stat().st_mtime)[-1]
        reps = parse_squat_reps(angle_csv_path, depth_threshold=depth_threshold)
        
        return jsonify({
            'success': True,
            'squat_reps': reps,
            'processing_time': elapsed,
            'depth_threshold': depth_threshold,
            'csv_file': str(angle_csv_path)
        })

    except Exception as e:
        logging.error(f"Error processing squat detection: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'squat-detection-api'})

if __name__ == "__main__":
    logging.basicConfig(
        format="%(message)s", level=logging.INFO, handlers=[logging.StreamHandler()]
    )
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)