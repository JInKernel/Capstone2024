FROM python:3.10.12-slim

# Copy the Django project files into the image 
COPY . /app 

# Set the working directory 
WORKDIR /app 

#Install Django and other required packages 
RUN pip install -r requirement.txt

# Start the Django development server 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
 
 