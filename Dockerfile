FROM python:3.6.1
ADD . /code
WORKDIR /code
RUN apt install libmysqlclient-dev
RUN pip install -r requirements.txt
CMD python bot/main.py