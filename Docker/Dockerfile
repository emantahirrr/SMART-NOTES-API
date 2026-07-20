# 1. Use an official Python runtime
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt
# 4. Copy the rest of your project files into the container
COPY . .

# 5. Expose the port your FastAPI app uses
EXPOSE 8000

# 6. Command to start the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
