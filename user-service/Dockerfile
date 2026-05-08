FROM python:3.9-slim
USER root
ENV GITHUB_TOKEN="ghp_1234567890abcdefghijklmnopqrstuvwxyz"
ENV AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5003
CMD python app.py
