FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade /code/requirements.txt

# add instructions for copying files in container and running them

# COPY . /code/

# RUN 