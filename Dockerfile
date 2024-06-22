FROM python:3.10.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy the Django project files into the image 
COPY . /app 

# Set the working directory 
# Set the working directory 
WORKDIR /app 

# Install Django, C++ compiler and other required packages 
RUN apt-get update && apt-get install -y default-libmysqlclient-dev gcc g++ pkg-config cmake libgl1-mesa-dev libglib2.0-0
RUN pip install -r requirements.txt
RUN pip install mysqlclient
RUN pip install mysql-connector-python
RUN pip install pillow
RUN pip install dlib
RUN pip install opencv-python

# Start the Django development server 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

EXPOSE 8000