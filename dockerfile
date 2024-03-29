FROM python:3.9

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV LIBRARY_DATA_PATH /app/books.json

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]

