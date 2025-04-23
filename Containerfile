# Use a Python base image
#FROM registry.access.redhat.com/ubi8/python-3.9:latest
FROM registry.redhat.io/ubi8/python-39

# Set working directory
WORKDIR /app

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLE_CORS=false

# Create a non-root user and switch to it
USER 1001

# Start the Streamlit application
CMD ["streamlit", "run", "main.py", "--server.address=0.0.0.0"]