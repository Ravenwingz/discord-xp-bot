# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the bot
CMD ["python3", "bot.py"]
