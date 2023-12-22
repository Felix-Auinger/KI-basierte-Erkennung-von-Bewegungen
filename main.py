import cv2
import numpy as np
from ultralytics import YOLO
import json
import os
import subprocess

# needs to be updated from 2D angles to 3D
def calculate_angle(A, B, C):
    # Vektoren AB und BC erstellen
    AB = B - A
    BC = C - B

    # Skalarprodukt und Normen berechnen
    dot_product = np.dot(AB, BC)
    norm_AB = np.linalg.norm(AB)
    norm_BC = np.linalg.norm(BC)

    # Winkel in Radiant berechnen
    angle = np.arccos(dot_product / (norm_AB * norm_BC))
    # Winkel in Grad umwandeln
    angle_deg = np.degrees(angle)
    return angle_deg

def get_keypoints(results):

    all_keypoints = []

    for frame_idx, r in enumerate(results):
        if r.keypoints and len(r.keypoints.xy) > 0:
            # Extract xy coordinates and confidence scores
            xy = r.keypoints.xy[0].cpu().numpy()  # Assuming the first set of keypoints corresponds to the detection
            confidences = r.keypoints.conf[0].cpu().numpy() if r.keypoints.conf is not None else [None] * len(xy)

            keypoints_list = []
            for (x, y), confidence in zip(xy, confidences):
                keypoints_list.extend([x, y, confidence if confidence is not None else 0])  # Adding 0 if confidence is None
            
            score = r.probs[0].item() if r.probs is not None else None  # Modify this line as needed

            # Convert each float32 value to a native Python float for JSON serialization
            keypoints_list = [float(val) for val in keypoints_list]

            # Estimate additional HALPE keypoints
            halpe_keypoints = estimate_additional_keypoints(keypoints_list)

            # Convert the box coordinates to numpy array and then to list
            if r.boxes and r.boxes.xyxy.shape[0] > 0:
                box = [float(val) for val in r.boxes.xyxy[0].cpu().numpy().tolist()]
            else:
                box = []


            keypoints_data = {
                "image_id": f"{frame_idx}.jpg",
                "category_id": 1, 
                "keypoints": halpe_keypoints,
                "score": float(score) if score is not None else None,
                "box": box, 
                "idx": [0.0] 
            }

            all_keypoints.append(keypoints_data)

    return all_keypoints

def estimate_additional_keypoints(keypoints):
        # Limit to the first 17 keypoints (x, y, confidence for each keypoint)
    if len(keypoints) >= 17 * 3:
        keypoints = keypoints[:17 * 3]
    else:
        return [0] * (17 * 3) 
    # Extract keypoints based on their indices from COCO format
    nose = keypoints[0:3]
    l_shoulder = keypoints[5 * 3:5 * 3 + 3]
    r_shoulder = keypoints[6 * 3:6 * 3 + 3]
    l_hip = keypoints[11 * 3:11 * 3 + 3]
    r_hip = keypoints[12 * 3:12 * 3 + 3]
    
    # Estimate the additional keypoints
    # 17 - Head (above the nose)
    head = [nose[0], nose[1] - 50, nose[2]]  # Adjust Y-offset as needed

    # 18 - Neck (midpoint between the shoulders)
    neck = [
        (l_shoulder[0] + r_shoulder[0]) / 2,
        (l_shoulder[1] + r_shoulder[1]) / 2,
        (l_shoulder[2] + r_shoulder[2]) / 2,
    ]

    # 19 - Hip (midpoint between the hips)
    hip = [
        (l_hip[0] + r_hip[0]) / 2,
        (l_hip[1] + r_hip[1]) / 2,
        (l_hip[2] + r_hip[2]) / 2,
    ]
    
    # For the remaining keypoints (big toes, small toes, heels), we can set them to the position of the ankles
    # since we do not have information on the feet from the upper body keypoints.
    # They should ideally be estimated from full body keypoints or set to a default value (like [0, 0, 0]).
    # Here, we use the ankle keypoints and apply a small offset.
    l_ankle = keypoints[15 * 3:15 * 3 + 3]
    r_ankle = keypoints[16 * 3:16 * 3 + 3]
    
    l_big_toe = [l_ankle[0], l_ankle[1] + 10, l_ankle[2]]
    r_big_toe = [r_ankle[0], r_ankle[1] + 10, r_ankle[2]]
    l_small_toe = [l_ankle[0] + 10, l_ankle[1], l_ankle[2]]
    r_small_toe = [r_ankle[0] + 10, r_ankle[1], r_ankle[2]]
    l_heel = [l_ankle[0], l_ankle[1] - 10, l_ankle[2]]
    r_heel = [r_ankle[0], r_ankle[1] - 10, r_ankle[2]]
    
    all_keypoints = keypoints[:17 * 3] + head + neck + hip + l_big_toe + r_big_toe + l_small_toe + r_small_toe + l_heel + r_heel
    return all_keypoints



def main():

    # Currently the best pose model from yolov8 is used
    # yolov8x-pose-p6.pt
    # Define model
    model = YOLO('./models/yolov8/yolov8x-pose-p6.pt')

     # Path to the directory containing videos
    video_dir = "./videos/todo"

    # Path to the output directory for MotionBERT results
    motionbert_output_dir = "./output/motionbert"

    # Ensure the output directory exists
    os.makedirs(motionbert_output_dir, exist_ok=True)

    # Iterate over each video file in the directory
    for video_file in os.listdir(video_dir):
        video_path = os.path.join(video_dir, video_file)

        # Process each video
        results = model(source=video_path, show=False, conf=0.3, save=False, stream=True)
        keypoints = get_keypoints(results)

        # Needs to be updated from 2D to 3d angels
        for r in results:
            if r.keypoints and r.keypoints.data.shape[1] >= 17:
                keypoints = r.keypoints.data[0].cpu().numpy()  # Konvertiere in numpy-Array

                right_shoulder = keypoints[6][:2]  # Index 6 rechte Schulter (X,Y)
                right_elbow = keypoints[8][:2]  # Index 8 rechter Ellbogen
                right_wrist = keypoints[10][:2]  # Index 10 rechtes Handgelenk

                angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
                angle_text = f"{angle:.2f} Grad"

                if r.orig_img is not None:
                    image = r.orig_img.copy()
                    cv2.putText(image, angle_text,
                                org=(int(right_elbow[0]), int(right_elbow[1])),
                                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                fontScale=1, color=(0, 255, 0), thickness=2)

                    cv2.imshow('Winkel Rechter Arm', image)
                    cv2.waitKey(1)

        # Save the keypoints data to a separate JSON file for each video
        json_filename = video_file.split('.')[0] + '_keypoints.json'  # Create a unique filename
        json_output_path = os.path.join('./outputs', json_filename)  # Path for the JSON file

        with open(json_output_path, 'w') as json_file:
            json.dump(keypoints, json_file, indent=4)

        # Run MotionBERT inference using the generated keypoints and the original video path
        motionbert_command = [
            'python', './MotionBert/infer_wild.py',
            '--vid_path', video_path,
            '--json_path', json_output_path,
            '--out_path', motionbert_output_dir
        ]

        try:
            subprocess.run(motionbert_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running MotionBERT: {e}")

if __name__ == "__main__":
    main()
