FROM python:3.11.0

WORKDIR /YEasy

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]