# -------------------------------------------------------------------
# 🧾 Dockerfile — Custom Jenkins Image with Docker-in-Docker (DinD) Support
# -------------------------------------------------------------------
# This Dockerfile extends the official Jenkins LTS image to enable
# Docker-in-Docker (DinD) capabilities, allowing Jenkins pipelines
# to build, test, and deploy Docker containers from within the Jenkins
# environment.
#
# 🔹 Summary of Steps
#   1. Base image: Use the stable Jenkins LTS version.
#   2. Privilege escalation: Switch to root to install dependencies.
#   3. Docker installation: Install Docker Engine, CLI, and runtime.
#   4. User configuration: Add the Jenkins user to the Docker group.
#   5. Volume setup: Create and mount /var/lib/docker for persistent storage.
#   6. Privilege reversion: Switch back to the Jenkins user for safety.
#
# 🧩 Usage
#   Build the image:
#       docker build -t custom-jenkins-dind .
#
#   Run Jenkins with Docker access:
#       docker run -d -p 8080:8080 \
#           -v /var/run/docker.sock:/var/run/docker.sock \
#           custom-jenkins-dind
#
# Notes
#   - Mounting /var/run/docker.sock allows Jenkins to access the host Docker daemon.
#   - Ensure Docker is installed on the host machine.
# -------------------------------------------------------------------


# -------------------------------------------------------------------
# 🧱 Base Image
# -------------------------------------------------------------------
FROM jenkins/jenkins:lts


# -------------------------------------------------------------------
# 🔧 Switch to root user to install dependencies
# -------------------------------------------------------------------
USER root


# -------------------------------------------------------------------
# 🐳 Install Docker Engine (for Docker-in-Docker builds)
# -------------------------------------------------------------------
RUN apt-get update -y && \
    apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        software-properties-common && \
    \
    # Add Docker’s official GPG key
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    \
    # Add Docker’s stable repository for Debian (Bullseye)
    echo "deb [arch=amd64] https://download.docker.com/linux/debian bullseye stable" \
        > /etc/apt/sources.list.d/docker.list && \
    \
    # Install Docker Engine and CLI tools
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    \
    # Clean up cache to reduce image size
    apt-get clean


# -------------------------------------------------------------------
# 👥 Configure Jenkins user permissions for Docker
# -------------------------------------------------------------------
RUN groupadd -f docker && \
    usermod -aG docker jenkins


# -------------------------------------------------------------------
# 📦 Setup Docker volume (for Docker-in-Docker)
# -------------------------------------------------------------------
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker


# -------------------------------------------------------------------
# 👤 Switch back to Jenkins user
# -------------------------------------------------------------------
USER jenkins