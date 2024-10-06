FROM python:3.9-slim

WORKDIR /server

COPY . /server


RUN pip install --no-cache-dir -r requirements.txt


# COPY text1.txt /server
# COPY text2.txt /server

CMD ["python3", "word_count_server.py"]
