FROM python:3.9-alpine

RUN mkdir /stock_app
RUN mkdir /stock_app/staticfiles
WORKDIR /stock_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt /stock_app/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /stock_app/entrypoint.sh
RUN chmod +x /stock_app/entrypoint.sh

COPY . .

ENTRYPOINT ["/stock_app/entrypoint.sh"]