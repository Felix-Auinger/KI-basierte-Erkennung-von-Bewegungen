import cv2
import numpy as np
from ultralytics import YOLO

def calculate_angle(A, B, C):
    AB = B - A
    BC = C - B
    dot_product = np.dot(AB, BC)
    norm_AB = np.linalg.norm(AB)
    norm_BC = np.linalg.norm(BC)
    angle = np.arccos(dot_product / (norm_AB * norm_BC))
    angle_deg = np.degrees(angle)
    return angle_deg


def check_pose(arm_angle, leg_angle):
    arm_correct = "Correct" if 140 <= arm_angle <= 180 else "Incorrect"
    leg_correct = "Correct" if 170 <= leg_angle <= 180 else "Incorrect"
    return arm_correct, leg_correct

def main():
    model = YOLO('yolov8n-pose.pt')
    results = model(source=0, show=True, conf=0.3, save=False, stream=True)

    for r in results:
        if r.keypoints and r.keypoints.data.shape[1] >= 17:
            keypoints = r.keypoints.data[0].numpy()

            right_shoulder = keypoints[6][:2]
            right_elbow = keypoints[8][:2]
            right_wrist = keypoints[10][:2]
            right_hip = keypoints[12][:2]
            right_knee = keypoints[14][:2]
            right_ankle = keypoints[16][:2]

            arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
            leg_angle = calculate_angle(right_hip, right_knee, right_ankle)
            hip_angle = calculate_angle(right_shoulder, right_hip, right_knee)

            arm_correct, leg_correct = check_pose(arm_angle, leg_angle)

            if r.orig_img is not None:
                image = r.orig_img.copy()

                cv2.putText(image, f"Arm Angle: {arm_angle:.2f}Deg ({arm_correct})",
                            (int(right_elbow[0]), int(right_elbow[1]) - 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
                cv2.putText(image, f"Leg Angle: {leg_angle:.2f}Deg ({leg_correct})",
                            (int(right_knee[0]), int(right_knee[1]) - 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (255, 0, 0), 2)
                cv2.putText(image, f"Hip Angle: {hip_angle:.2f}Deg",
                            (int(right_hip[0]), int(right_hip[1]) - 20),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 0, 255), 2)

                cv2.putText(image, f"Right Shoulder: ({int(right_shoulder[0])}, {int(right_shoulder[1])})",
                            (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"Right Elbow: ({int(right_elbow[0])}, {int(right_elbow[1])})",
                            (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"Right Wrist: ({int(right_wrist[0])}, {int(right_wrist[1])})",
                            (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"Right Hip: ({int(right_hip[0])}, {int(right_hip[1])})",
                            (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"Right Knee: ({int(right_knee[0])}, {int(right_knee[1])})",
                            (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.putText(image, f"Right Ankle: ({int(right_ankle[0])}, {int(right_ankle[1])})",
                            (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                cv2.imshow('Pose Estimation with Angles and Coordinates - SportDx', image)
                cv2.waitKey(1)

if __name__ == "__main__":
    main()
