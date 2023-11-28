import cv2
import numpy as np
from ultralytics import YOLO
import json


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

def main():
    model = YOLO('yolov8n-pose.pt')
    results = model(source="test5.mp4", show=False, conf=0.3, save=False, stream=True)

    all_keypoints = []  # List to store all keypoints data

    for frame_idx, r in enumerate(results):
        if r.keypoints and len(r.keypoints.xy) > 0:
            # Extract xy coordinates and confidence scores
            xy = r.keypoints.xy[0].cpu().numpy()  # Assuming the first set of keypoints corresponds to the detection
            confidences = r.keypoints.conf[0].cpu().numpy() if r.keypoints.conf is not None else [None] * len(xy)

            keypoints_list = []
            for (x, y), confidence in zip(xy, confidences):
                keypoints_list.extend([x, y, confidence or 0])  # Adding 0 if confidence is None
            
            score = r.probs[0].item() if r.probs is not None else None  # Modify this line as needed

            # Convert each float32 value to a native Python float for JSON serialization
            keypoints_list = [float(val) for val in keypoints_list]

            # Convert the box coordinates to numpy array and then to list
            # Choose the appropriate format (xyxy, xywh, etc.) as per your requirement
            # Assuming you're using xyxy format for the box
            box = [float(val) for val in r.boxes.xyxy[0].cpu().numpy().tolist()] if r.boxes is not None else []

            # Format the data as per your JSON structure
            keypoints_data = {
                "image_id": f"{frame_idx}.jpg",
                "category_id": 1,  # Assuming category_id is 1 for all, modify as needed
                "keypoints": keypoints_list,
                "score": float(score) if score is not None else None,
                "box": box, 
                "idx": [0.0] 
            }

            all_keypoints.append(keypoints_data)

    # Save the keypoints data to a JSON file
    with open('keypoints_output.json', 'w') as f:
        json.dump(all_keypoints, f, indent=4)

    for r in results:
        if r.keypoints and r.keypoints.data.shape[1] >= 17:
            keypoints = r.keypoints.data[0].numpy()  # Konvertiere in numpy-Array

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


if __name__ == "__main__":
    main()
