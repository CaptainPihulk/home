FROM python:3.10-alpine

COPY ./requirements.txt /src/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /src/requirements.txt

COPY . /src

EXPOSE 6060
ENV MY_ENV=netology
WORKDIR src

CMD ["python3", "manage.py", "runserver", "0.0.0.0:6060"]

