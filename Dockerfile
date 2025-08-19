# Base Python image
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    python3-dev \
    bash \
    nginx \
    zbar-tools \
    libgl1 \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# -------------------- Backend Setup --------------------
# Install uv package manager
RUN pip install --no-cache-dir uv

# Install Python dependencies
COPY BackEnd/analyze/requirements.txt ./BackEnd/analyze/requirements.txt
RUN uv pip install --system -r ./BackEnd/analyze/requirements.txt

# Copy backend code
COPY ./BackEnd/ ./BackEnd/

# -------------------- Frontend Setup --------------------
COPY ./FrontEnd/ ./FrontEnd/

# -------------------- NGINX Setup --------------------
# NGINX configuration
COPY /nginx.conf /etc/nginx/nginx.conf

# Copy and prepare startup script
COPY ./BackEnd/start_server.sh ./BackEnd/start_server.sh
RUN sed -i 's/\r$//' ./BackEnd/start_server.sh && chmod +x ./BackEnd/start_server.sh

# Expose NGINX port
EXPOSE 8080

# Start server
WORKDIR /app/BackEnd
CMD ["./start_server.sh"]