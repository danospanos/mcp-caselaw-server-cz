# Use Python 3.12 slim image (Debian-based)
FROM python:3.12-slim

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Create virtual environment in /opt instead of /app to avoid volume mount conflicts
RUN python -m venv /opt/venv

# Activate virtual environment and upgrade pip
RUN /opt/venv/bin/pip install --upgrade pip

# Install Python packages in the virtual environment
RUN /opt/venv/bin/pip install requests fastmcp uvicorn beautifulsoup4 markdownify

# Set PATH to use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY server.py .

# Expose port 8000 for the HTTP server
EXPOSE 8000

# Run the FastMCP server with Uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
