FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install .
CMD ["alembic", "upgrade", "head"]
CMD ["python", "-m", "rpgdiscordhelper.main"]
