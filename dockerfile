# Use an NVIDIA CUDA base image with PyTorch support
#FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime

# Start from a PyTorch base image for Jetson (L4T) compatible with ARM
FROM nvcr.io/nvidia/l4t-pytorch:r32.4.4-pth1.6-py3

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies including gcc and other build tools
#RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y xfce4 
#RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y build-essential  
#RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y libfreetype6-dev 
#RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y libpng-dev      
#RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y pkg-config 
#RUN rm -rf /var/lib/apt/lists/*

# Clone the GitHub repository recursively ( only if you dont already have the github)
# RUN git clone --recurse-submodules -b development_mark https://github.com/Felix-Auinger/KI-basierte-Erkennung-von-Bewegungen.git

# Change working directory to the cloned repo
WORKDIR /usr/src/app/KI-basierte-Erkennung-von-Bewegungen
# Copy current dir
#COPY . .

# Install Python dependencies
RUN pip install torchvision \
    torchaudio \ 
    tensorboardX \
    tqdm \
    easydict  \
    prettytable  \
    chumpy  \
    opencv-python  \
    imageio-ffmpeg  \
    matplotlib==3.1.1  \
    roma  \
    ipdb  \
    pytorch-metric-learning  \
    smplx[all]
RUN pip install ultralytics


# Create dirs
#RUN mkdir -p ./videos/todo
#RUN mkdir -p ./outputs/motionbert
# Copy videos and files
#COPY videos/todo/* ./videos/todo/
#COPY configs ./MotionBERT4sportDX/configs/pose3d/
#COPY checkpoints  ./MotionBERT4sportDX/checkpoint/pose3d/

# Expose any necessary ports
#EXPOSE 80

# Define environment variable if needed
ENV NAME sportdx

# Command to run the application
#CMD ["python", "main.py"]
