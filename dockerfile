# Use an NVIDIA CUDA base image with PyTorch support
FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-runtime

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies including gcc and other build tools
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git \
    xfce4 \
    build-essential \  
    libfreetype6-dev \ 
    libpng-dev \      
    pkg-config \  
    ffmpeg \    
    && rm -rf /var/lib/apt/lists/*

# Clone the GitHub repository recursively
RUN git clone --recurse-submodules -b development_motionBert_mark https://github.com/Felix-Auinger/KI-basierte-Erkennung-von-Bewegungen.git

# Change working directory to the cloned repo
WORKDIR /usr/src/app/KI-basierte-Erkennung-von-Bewegungen

# Install Python dependencies
RUN pip install torchvision torchaudio 
RUN pip install -r requirements.txt
RUN pip install ultralytics

# Create dirs
RUN mkdir -p ./videos/todo
RUN mkdir -p ./outputs/motionbert

# Copy videos and files
COPY videos/todo/* ./videos/todo/
COPY configs ./MotionBERT4sportDX/configs/pose3d/
COPY checkpoints  ./MotionBERT4sportDX/checkpoint/pose3d/

# Expose any necessary ports
EXPOSE 80

# Define environment variable if needed
ENV NAME World

# Command to run the application
#CMD ["python", "main.py"]
