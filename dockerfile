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

# Clone the GitHub repository recursively ( only if you dont already have the github)
# RUN git clone --recurse-submodules -b development_mark https://github.com/Felix-Auinger/KI-basierte-Erkennung-von-Bewegungen.git

# Change working directory to the cloned repo
WORKDIR /usr/src/app/KI-basierte-Erkennung-von-Bewegungen
# Copy current dir
#COPY . .

# Install Python dependencies
#RUN pip install torchvision \
#    torchaudio \ 
#    tensorboardX \
#    tqdm \
#    easydict  \
#   prettytable  \
#    chumpy  \
#    opencv-python  \
#    imageio-ffmpeg  \
#    matplotlib==3.1.1  \
#    roma  \
#    ipdb  \
#    pytorch-metric-learning  \
#    smplx[all]
#RUN pip install ultralytics


# Install Python dependencies using Conda and pip as a fallback
RUN conda install -c pytorch torchvision
RUN conda install -c pytorch torchaudio
RUN conda install -c pytorch tensorboardX
RUN conda install -c pytorch tqdm
RUN conda install -c conda-forge easydict 
RUN conda install -c conda-forge prettytable 
RUN conda install -c conda-forge chumpy 
RUN conda install -c conda-forge opencv 
RUN conda install -c conda-forge matplotlib==3.1.1
RUN conda install -c conda-forge roma
RUN conda install -c conda-forge ipdb

# Install the ultralytics package using conda
RUN conda install -c conda-forge ultralytics


# Create dirs
#RUN mkdir -p ./videos/todo
#RUN mkdir -p ./outputs/motionbert
# Copy videos and files
#COPY videos/todo/* ./videos/todo/
#COPY configs ./MotionBERT4sportDX/configs/pose3d/
#COPY checkpoints  ./MotionBERT4sportDX/checkpoint/pose3d/

# Expose any necessary ports
EXPOSE 80

# Define environment variable if needed
ENV NAME sportdx

# Command to run the application
#CMD ["python", "main.py"]
