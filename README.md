# SportDX Docker Container Setup

This document provides instructions for building and running the `sportdx` Docker container, which is set up for GPU-accelerated PyTorch applications with GUI support via WSL2.

## Prerequisites

- Windows 10 or 11 with WSL2 enabled.
- NVIDIA GPU with the latest drivers installed.
- Docker Desktop for Windows with WSL2 backend and NVIDIA Container Toolkit.

## Building the Docker Image

1. Open WSL2 and navigate to the directory containing the Dockerfile.
2. Build the Docker image:
   ```bash
   docker build -t sportdx .
   ```

## Running the Docker Container

To run the `sportdx` container with GPU and GUI support:

1. Allow local connections to the X server:
   ```bash
   xhost +local:docker
   ```

2. Run the container:
   ```bash
   docker run -it --gpus all -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix sportdx
   ```

## Starting an Existing Container

If the container `sportdx` is already created and you want to start it:

1. Start the container:
   ```bash
   docker start sportdx
   ```

2. Attach to the container for interaction:
   ```bash
   docker attach sportdx
   ```

## Folder Structure

```
├── checkpointscheckpoints\FT_MB_lite_MB_ft_h36m_global_lite\ *Place motionbert checkpoint here*
├── configs *place config motionBert here*
├── models *yolov8 model will be here*
├── MotionBERT4sportDX *Motionbert fork*
├── outputs *outputs from yolov8 and motionbert*
├── videos/todo *add videos here*
├── dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## Notes

- The command `xhost +local:docker` opens up the X server for local connections and should be used with caution due to potential security implications.
- The Docker setup is advanced and might require specific configurations based on your hardware and software environment.
- Ensure that your WSL2 and Docker Desktop are properly configured for GPU acceleration.

