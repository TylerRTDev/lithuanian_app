FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 5000

COPY entrypoint.sh /entrypoint.sh

# 9. Make entrypoint script executable
RUN chmod +x /entrypoint.sh

# 10. Set entrypoint to the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]