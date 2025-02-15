# Use a base image that includes both Python and Node.js, or install them manually
FROM python:3.12-slim-bookworm

# Install Node.js curl and sqlite
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates gnupg
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install sqlite3

# Download and install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# install duckdb
RUN curl install.duckdb.org | sh

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin:$PATH"

# Set up the application directory
WORKDIR /app
RUN mkdir -p /data && chmod 777 /data

# Copy application files
COPY main.py /app
COPY tasksA.py /app
COPY tasksB.py /app

# Explicitly set the correct binary path and use `sh -c`
CMD ["/root/.local/bin/uv", "run", "main.py"]