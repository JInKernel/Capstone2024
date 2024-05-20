FROM python:3.10.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the Django project files into the image 
COPY . /app 

# Set the working directory 
WORKDIR /app 

#Install Django and other required packages 
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc pkg-config
RUN pip install -r requirements.txt
RUN pip install mysqlclient
RUN pip install mysql-connector-python

# Start the Django development server 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000
 
 