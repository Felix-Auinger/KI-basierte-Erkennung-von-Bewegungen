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
    results = model(source=0, show=True, conf=0.3, save=False, stream=True)

    for r in results:
        if r.keypoints and r.keypoints.data.shape[1] >= 17:
            keypoints = r.keypoints.data[0].numpy()  # Konvertiere in numpy-Array

            # Koordinaten für die rechte Körperseite
            right_shoulder = keypoints[6][:2]  # Index 6 rechte Schulter
            right_elbow = keypoints[8][:2]  # Index 8 rechter Ellbogen
            right_wrist = keypoints[10][:2]  # Index 10 rechtes Handgelenk
            right_hip = keypoints[12][:2]  # Index 12 rechte Hüfte
            right_knee = keypoints[14][:2]  # Index 14 rechtes Knie
            right_ankle = keypoints[16][:2]  # Index 16 rechter Knöchel

            # Berechnung der Winkel
            arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            leg_angle = calculate_angle(right_hip, right_knee, right_ankle)
            hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)

            if r.orig_img is not None:
                image = r.orig_img.copy()
                cv2.putText(image, f"Arm: {arm_angle:.2f}Grad",
                            (int(right_elbow[0]), int(right_elbow[1])),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
                cv2.putText(image, f"Bein: {leg_angle:.2f}Grad",
                            (int(right_knee[0]), int(right_knee[1])),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 0), 2)
                cv2.putText(image, f"Huefte: {hip_angle:.2f}Grad",
                            (int(right_hip[0]), int(right_hip[1])),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 2)

                # Bild mit den Winkeln anzeigen
                cv2.imshow('Winkel Rechte Seite', image)
                cv2.waitKey(1)

if __name__ == "__main__":
    main()
