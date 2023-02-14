FROM python:3.11.0
WORKDIR /YEasy
RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 8080/tcp