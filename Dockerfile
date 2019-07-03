FROM python:3.6.1
ADD . /code
WORKDIR /code
RUN apt install libmysqlclient-dev
RUN pip install -r requirements.txt
RUN adduser myuser
USER myuser
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
CMD python bot/test_conv.py
