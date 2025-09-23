# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy only necessary files
COPY requirements.txt ./
COPY rpgserver.py ./
COPY roomlogic.py ./
COPY usercommands.py ./
COPY world.json ./
COPY endgame.json ./
COPY templates/ ./templates/
COPY images/ ./images/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5006

# Run the Flask app
CMD ["python", "rpgserver.py"]
