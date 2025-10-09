# 🧾 Dockerfile — Custom Jenkins (Docker-in-Docker)

This Dockerfile builds a **custom Jenkins image** with **Docker-in-Docker (DinD)** capabilities, allowing Jenkins pipelines to **build, test, and deploy Docker containers** directly within the Jenkins environment.

It extends the official **Jenkins LTS** image and adds everything needed for containerised CI/CD workflows, such as Docker Engine and CLI tools.

## 📁 File Location

```
mlops-hotel-reservation-prediction/
├── custom_jenkins/
│   └── Dockerfile
└── Jenkinsfile
```

## ⚙️ Purpose

This image is used in the **CICD Pipeline** stage of the project to enable Jenkins to:

* Run builds in isolated containers.
* Build and tag new Docker images.
* Push images to a remote registry (e.g. Google Cloud Registry or DockerHub).
* Deploy applications to container platforms such as Cloud Run or Kubernetes.

Without this configuration, Jenkins would not have permission or tooling to execute Docker commands from within its own container.

## 🧩 Build & Run Instructions

### 1. Build the image

```bash
docker build -t custom-jenkins-dind ./custom_jenkins
```

### 2. Run Jenkins with Docker access

```bash
docker run -d -p 8080:8080 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    custom-jenkins-dind
```

* Port `8080` exposes the Jenkins UI.
* Mounting `/var/run/docker.sock` gives Jenkins access to the host Docker daemon.
* Ensure Docker is installed and running on the host machine.

## 🧱 Key Build Steps

| Step                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| **Base Image**             | Starts from the stable `jenkins/jenkins:lts` image.                      |
| **Privilege Escalation**   | Switches to `root` to install dependencies.                              |
| **Install Docker Engine**  | Installs `docker-ce`, `docker-ce-cli`, and `containerd.io`.              |
| **User Permissions**       | Adds the `jenkins` user to the `docker` group for Docker command access. |
| **Volume Setup**           | Creates and mounts `/var/lib/docker` for Docker-in-Docker builds.        |
| **Revert to Jenkins User** | Returns control to the non-root `jenkins` user for security.             |

## 🧰 Packages Installed

* `apt-transport-https`
* `ca-certificates`
* `curl`
* `gnupg`
* `software-properties-common`
* `docker-ce`
* `docker-ce-cli`
* `containerd.io`

## 🧠 How It Works

When Jenkins runs inside this container:

1. It inherits Docker client access via the mounted socket.
2. Jenkins jobs can safely execute Docker commands (`build`, `push`, `run`) within CI pipelines.
3. The DinD setup allows nested container workflows, useful for automated builds and cloud deployments.

Example pipeline step:

```groovy
stage('Build Docker Image') {
    steps {
        sh 'docker build -t myapp:latest .'
        sh 'docker push gcr.io/myproject/myapp:latest'
    }
}
```

## 🛡️ Security Notes

* Use this image **only on trusted CI/CD hosts** (since the mounted Docker socket gives root-level access to the host).
* Keep the image updated with the latest Jenkins LTS and Docker versions.
* Restrict Jenkins access to authorised users.

## ✅ Summary

| Feature            | Description                              |
| ------------------ | ---------------------------------------- |
| **Base Image**     | `jenkins/jenkins:lts`                    |
| **Docker Support** | Full Docker Engine + CLI inside Jenkins  |
| **Use Case**       | Build and deploy containers from Jenkins |
| **Volume**         | `/var/lib/docker` for persistent builds  |
| **Port**           | 8080 (Jenkins Web UI)                    |
