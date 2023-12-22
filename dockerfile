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
    && rm -rf /var/lib/apt/lists/*

# Clone the GitHub repository recursively
RUN git clone --recurse-submodules -b development_motionBert_mark https://github.com/Felix-Auinger/KI-basierte-Erkennung-von-Bewegungen.git

# Change working directory to the cloned repo
WORKDIR /usr/src/app/KI-basierte-Erkennung-von-Bewegungen

# List the contents of the directory to verify the presence of requirements.txt
RUN ls -la

# Install Python dependencies
RUN pip install torchvision torchaudio 
RUN pip install -r requirements.txt
RUN pip install ultralytics

# Create videos/todo directory and copy them into the container
RUN mkdir -p ./videos/todo
COPY videos/todo/* ./videos/todo/

RUN mkdir -p ./outputs/motionbert

# Copy the configs directory to the Docker image
COPY configs ./MotionBERT/configs/pose3d/
COPY checkpoints  ./MotionBERT/checkpoint/pose3d/

# Expose any necessary ports
EXPOSE 80

# Define environment variable if needed
ENV NAME World

# Command to run the application
#CMD ["python", "your_script.py"]
