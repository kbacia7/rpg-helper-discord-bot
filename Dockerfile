FROM python:3
WORKDIR /usr/src/app
RUN pip install .
COPY . .
CMD ["python", "-m ", "rpgdiscordhelper.main "]
