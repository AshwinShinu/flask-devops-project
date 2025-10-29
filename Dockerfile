FROM python:3.10-slim

WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app

ENV DATABASE_URL=sqlite:///database.db
EXPOSE 5000

# Use gunicorn for production-like behavior
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers=2"]
