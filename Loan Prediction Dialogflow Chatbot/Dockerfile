#start from python base image
From python:3.10.6

# change working directory
WORKDIR /code

#add requirements file to image
COPY ./requirements.txt /code/requirements.txt

#install python libraries
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#add python code
COPY ./app/ /code/app

# Set the environment variable for Flask ENV 
ENV FLASK_APP=app/main.py

# Specify default commands 
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]