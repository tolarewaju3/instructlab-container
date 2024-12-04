# Fedora + InstructLab
# https://github.com/instructlab/instructlab

# Build the image: podman build -t instructlab:latest -f Containerfile .

# Use the latest Fedora image
FROM fedora:latest

# Install dependencies
RUN dnf install -y cmake python-devel gcc gcc-c++ make git python3.11 python3.11-devel python3-pip
RUN mkdir instructlab
WORKDIR instructlab

# Install InstructLab using PyTorch without CUDA bindings and no GPU acceleration
RUN pip install instructlab --extra-index-url=https://download.pytorch.org/whl/cpu -C cmake.args="-DLLAMA_NATIVE=off"

# Configure ilab
RUN ilab config init --non-interactive
RUN ilab model download

# Change ilab configuration
COPY config.yaml .
#RUN ilab model serve

EXPOSE 8000

ENTRYPOINT ["ilab", "model", "serve"]

#ENTRYPOINT ["/bin/sh"]
#Run the container: podman run -d --name instructlab -p 8000:8000 instructlab:latest ilab model serve
