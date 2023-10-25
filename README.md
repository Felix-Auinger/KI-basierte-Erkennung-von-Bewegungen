# KI-basierte Erkennung von Bewegungen

## Voraussetzungen


- **Python:** Version >= 3.8
- **PyTorch:** Version >= 1.8

Hatte bei mir WSL2 Ubunutu 22 auf Win10 (sollte jedoch auf ähnlichen Systemen funktionieren)

![Bild zur Demonstration](./images/image.png)

## Installation

1. Installieren von PyTorch und zugehörigen Paketen:

```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

2. Ultralytics Bibliothek installieren:

```
pip3 install ultralytics
```

## Erster Test

Um sicherzustellen, dass alles korrekt installiert wurde, führen Sie den folgenden Befehl aus:

```
yolo predict model=yolov8n.pt source='https://ultralytics.com/images/bus.jpg'
```

Die Modellcheckpoints werden automatisch heruntergeladen. 

## Pose Estimation Modelle

Hier finden Sie eine Auflistung aller Pose Estimation Modelle:

![Liste der Pose Estimation Modelle](./images/image-1.png)

Die oberen Modelle sind in der Regel schneller, aber möglicherweise ungenauer.

Um eine Inference mit einem anderen Bild oder Video zu starten, ersetzen Sie einfach den Wert in `source=''` und passen Sie gegebenenfalls das Modell an:

yolo predict model=yolov8n-pose.pt source=test.mp4