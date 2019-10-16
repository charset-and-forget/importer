FROM python:3.7

WORKDIR /usr/src/app

COPY src/ ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pycodestyle ./

CMD python script.py
