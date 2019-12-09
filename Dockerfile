FROM python:3.6
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash -
RUN apt install npm
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
#ADD code/ /code/
#RUN mkdir /media
VOLUME /media
VOLUME /code
