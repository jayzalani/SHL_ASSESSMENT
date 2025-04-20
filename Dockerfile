FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Create logs directory
RUN mkdir -p logs

# Set environment variables
ENV PORT=8080

# Run the application
CMD exec python main.py --mode api