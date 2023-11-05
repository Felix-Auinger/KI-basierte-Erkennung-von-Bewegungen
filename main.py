import cv2
import numpy as np
from ultralytics import YOLO


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
    results = model(source=0, show=False, conf=0.3, save=False, stream=True)

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
