# Stage 1: Build environment for scraping

FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    sqlite3 \
    && apt-get clean

# Install Chrome and other dependencies
RUN apt-get update && apt-get install -y wget unzip net-tools lsof && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

WORKDIR /app

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scraping script and its dependencies
COPY accupass.py .

COPY app.py .

# Example: Initialize SQLite database schema (if needed)
RUN sqlite3 scrapedata.db < init.sql

# Copy the rest of the application
COPY . .

# Example: Initialize SQLite database schema (if needed)
RUN sqlite3 scrapedata.db < init.sql

EXPOSE 5000

CMD ["bash", "-c", "python accupass.py & python app.py"]
