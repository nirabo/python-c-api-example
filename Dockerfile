# Multi-stage build for Python 2.7 C-API development environment

# Build stage: compile and build everything
FROM ubuntu:18.04 AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python2.7 \
    python2.7-dev \
    python-pip \
    python-setuptools \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Jupyter dependencies in one layer
RUN pip install --no-cache-dir --upgrade pip==20.3.4 setuptools==44.1.1 && \
    pip install --no-cache-dir ipython==5.10.0 notebook==5.7.16 jupyter-console==5.2.0 ipykernel==4.10.1 \
    jupyter-client==5.3.5 nbconvert==5.6.1 widgetsnbextension==3.6.6

# Copy source code and build C extension
WORKDIR /app
COPY src/ ./src/
COPY setup.py .
RUN python2.7 setup.py build_ext --inplace

# Runtime stage: development environment with build tools
FROM ubuntu:18.04 AS runtime

# Install runtime and build dependencies for development
RUN apt-get update && apt-get install -y --no-install-recommends \
    python2.7 \
    python2.7-dev \
    python-setuptools \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python2.7/dist-packages/ /usr/local/lib/python2.7/dist-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Set up working directory and copy project files
WORKDIR /app
COPY . /app

# Copy built C extension from builder
COPY --from=builder /app/*.so /app/

# Set Python 2.7 as default and create Jupyter config
RUN ln -sf /usr/bin/python2.7 /usr/bin/python && \
    mkdir -p /root/.jupyter

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH=/app

# Expose Jupyter port
EXPOSE 8888

# Default command
CMD ["/bin/bash"]
