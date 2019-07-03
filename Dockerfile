FROM python:3.6.1
ADD . /code
WORKDIR /code
RUN apt install libmysqlclient-dev
RUN pip install -r requirements.txt
RUN adduser myuser
USER myuser
CMD python bot/main.py
