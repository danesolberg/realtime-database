FROM python:3.9-alpine

WORKDIR .

COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

COPY server/ ./server
COPY main.py .

CMD [ "python", "./main.py" ]