# testing squat pose detection

import toml
import logging
import logging.handlers
import pandas as pd
from pathlib import Path
import numpy as np
from datetime import datetime

from sports2d import Sports2D

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


def main():
    # 1) Load config
    config_path = "config.toml"  # or "Config_demo.toml", etc.
    try:
        config_dict = toml.load(config_path)
    except FileNotFoundError:
        logging.warning(
            f"No config file found at {config_path}; using default Sports2D logic."
        )
        config_dict = {}

    # 2) Override key fields for *webcam* usage
    # Make sure we have the minimal structure
    config_dict.setdefault("project", {})
    config_dict.setdefault("process", {})

    # Force usage of the webcam
    config_dict["project"]["video_input"] = "webcam"

    # Ensure real-time results
    config_dict["process"]["show_realtime_results"] = True

    # (Optional) single person to keep it simpler
    config_dict["process"]["multiperson"] = False

    # 3) Run the main sports2d pipeline
    # This will open a webcam feed in a window & produce CSV angle files upon completion
    start_time = datetime.now()
    Sports2D.process(config_dict)  # offline => no per-frame callback

    elapsed = (datetime.now() - start_time).total_seconds()
    logging.info(f"Pose + angle processing finished in {elapsed:.1f} seconds.")

    # 4) After finishing, parse the CSV for your squat analysis
    #    Typically, Sports2D saves angles to something like:
    #       <video_basename>_<pose_model>_person0_angles.csv
    #    But if it's a webcam, the name might vary. We can search for "person0_angles.csv"
    #    in the configured result directory.

    result_dir = config_dict["process"].get("result_dir", "")
    if not result_dir:
        result_dir = Path.cwd()
    else:
        result_dir = Path(result_dir).resolve()

    angle_csv_list = list(result_dir.glob("*person0_angles.csv"))
    if not angle_csv_list:
        logging.warning(
            "No angle CSV file found. Possibly no frames were recorded, or naming differs."
        )
        return

    # We assume the last produced file is our new result
    angle_csv_path = sorted(angle_csv_list, key=lambda x: x.stat().st_mtime)[-1]
    reps = parse_squat_reps(angle_csv_path, depth_threshold=90)
    logging.info(f"\nTotal squat reps (offline analysis) = {reps}\n")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(message)s", level=logging.INFO, handlers=[logging.StreamHandler()]
    )
    main()