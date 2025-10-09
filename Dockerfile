# -------------------------------------------------------------------
# 🧱 Base Image
# -------------------------------------------------------------------
FROM python:3.13-slim

# -------------------------------------------------------------------
# 🛠️ Environment
# -------------------------------------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory
WORKDIR /app

# -------------------------------------------------------------------
# 📦 System dependencies
# - libgomp1 is required by LightGBM
# -------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# -------------------------------------------------------------------
# 🔧 Python deps (install wheels first to avoid building from source)
# Install pyarrow explicitly so it resolves to a prebuilt wheel on 3.13
# -------------------------------------------------------------------
RUN python -m pip install --upgrade pip \
 && pip install "pyarrow==21.0.0"

# -------------------------------------------------------------------
# 📂 Copy project and install package
# (If you have a requirements.txt or pyproject, you can copy+install
#  those earlier to leverage build cache; this keeps it simple.)
# -------------------------------------------------------------------
COPY . .

# Install your package in editable mode
RUN pip install -e .

# -------------------------------------------------------------------
# 🧪 Optional: Train the model at build time 
#    Note: many teams run training as a separate CI job or at runtime
#          rather than during image build.
# -------------------------------------------------------------------
RUN python pipeline/training_pipeline.py

# -------------------------------------------------------------------
# 🌐 Runtime
# -------------------------------------------------------------------
EXPOSE 8080
CMD ["python", "app.py"]