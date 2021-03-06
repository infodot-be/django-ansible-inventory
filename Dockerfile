FROM python:3.6
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
ADD code/ /code
RUN mkdir media
COPY entrypoint.sh /code

RUN chmod +x /code/entrypoint.sh

# outsite port
EXPOSE 8000

# run entrypoint.sh
ENTRYPOINT ["/code/entrypoint.sh"]
