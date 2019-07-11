FROM python:3.6.1
ADD . /code
WORKDIR /code
RUN apt install libmysqlclient-dev
RUN pip install -r requirements.txt
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN adduser myuser
USER myuser
CMD python bot/test_db.py
