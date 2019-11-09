FROM python:3
WORKDIR /usr/src/app
RUN pip install PyYAML discord.py pytimeparse --no-cache-dir
COPY . .
CMD ["python", "./main.py"]
