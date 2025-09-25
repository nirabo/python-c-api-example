FROM ubuntu:18.04

# Install Python 2.7 and development tools
RUN apt-get update && apt-get install -y \
    python2.7 \
    python2.7-dev \
    python-pip \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Jupyter and IPython for Python 2.7 (compatible versions)
RUN pip install --upgrade pip && \
    pip install ipython==5.10.0 notebook==5.7.16 jupyter-console==5.2.0 ipykernel==4.10.1 \
    jupyter-client==5.3.5 nbconvert==5.6.1 widgetsnbextension==3.6.6

# Create a working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Set Python 2.7 as default python
RUN ln -sf /usr/bin/python2.7 /usr/bin/python

# Create Jupyter config directory
RUN mkdir -p /root/.jupyter

# Build the C extension module
RUN python setup.py build_ext --inplace

# Expose Jupyter port
EXPOSE 8888

# Install any Python dependencies if needed
# RUN pip install -r requirements.txt

# Default command
CMD ["/bin/bash"]
