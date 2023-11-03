from ultralytics import YOLO


def main():
    model = YOLO('yolov8n-pose.pt')

    results = model(source=0, show=True, conf=0.3, save=False)


if __name__ == "__main__":
    main()
