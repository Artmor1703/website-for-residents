FROM python:3.10.9

ENV PYTHONBUFFER=1

WORKDIR /TSG/manage.py

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY  . .

EXPOSE 8000

CMD python TSG/manage.py runserver 0.0.0.0:8000