FROM python:3.9.18

WORKDIR /app


COPY . .


ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql"
ENV MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"
ENV DB_USE="root"
ENV DB_PASS="02136"
ENV HOST_NAME="34.27.144.61"

RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

#RUN python3 -m pip install python-csv

RUN pip install django

RUN pip install python-dotenv

RUN apt-get install libcairo2-dev -y

RUN pip install -r requirement.txt

RUN pip install xhtml2pdf

RUN python3 manage.py

RUN python3 manage.py makemigrations 

RUN python3 manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
