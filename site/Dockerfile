FROM python:3.6
WORKDIR /usr/source/app
COPY requirements.txt .
RUN pip3 install  -r requirements.txt
COPY . .
CMD ["python", "main.py"]
