FROM python:3.6
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
ADD code/ /
RUN mkdir media
COPY entrypoint.sh /

RUN chmod +x /entrypoint.sh

# outsite port
EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
