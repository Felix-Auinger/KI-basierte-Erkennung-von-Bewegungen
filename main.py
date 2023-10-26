import cv2
from ultralytics import YOLO

def main():
    """
    Primary Prototype of Webcam Based YoloV8 Pose Detection
    """


# Load the YOLOv8 model
    model = YOLO('yolov8n-pose.pt')

    # Open camera
    cap = cv2.VideoCapture(0)

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            print("Error in Live Detection or Webcam")

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
