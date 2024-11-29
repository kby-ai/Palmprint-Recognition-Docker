FROM ubuntu:20.04

# Install system dependencies, including Python and pip
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    python3.8 \
    python3-pip \
    libjpeg8 \
    libwebp6 \
    libpng16-16 \
    libtbb2 \
    libtiff5 \
    libtbb-dev \
    unzip \
    libopenexr-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ensure pip is installed
RUN python3.8 -m pip install --upgrade pip

# Set up working directory
RUN mkdir -p /root/kby-ai-palmprint
WORKDIR /root/kby-ai-palmprint

# Copy shared libraries and application files
COPY ./libhand.so /usr/local/lib/
COPY ./libopencv.zip .
RUN unzip libopencv.zip
RUN cp -f libopencv/* /usr/local/lib/ 
RUN ldconfig

# Copy Python and application files
COPY ./handtool-0.2.1-py3-none-any.whl .
COPY ./app.py .
COPY ./roi.py .
COPY ./requirements.txt .
COPY ./run.sh .
COPY ./img ./img

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN chmod +x ./run.sh
# Set up entrypoint
CMD ["/root/kby-ai-palmprint/run.sh"]

# Expose ports
EXPOSE 8080 9000