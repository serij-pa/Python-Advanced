FROM python:3.9.19-slim

RUN mkdir /app_n_y_a

COPY .  ./app_n_y_a/

#COPY requirements.txt /app/

RUN python -m pip install -r /app_n_y_a/requirements.txt

#COPY app.py /app/

WORKDIR /app_n_y_a

ENTRYPOINT ["python", "app.py"]
