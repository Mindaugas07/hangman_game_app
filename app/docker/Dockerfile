# syntax=docker/dockerfile:1

# start by pulling the python image
FROM python:3.8-alpine

# copy the requirements file into the image
COPY app/docker/requirements.txt /requirements.txt

# switch working directory
WORKDIR /app/docker

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app/docker

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["app.py" ]