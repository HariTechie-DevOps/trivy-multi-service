FROM python:3.9-slim
USER root
ENV SENDGRID_API_KEY="SG.xxxxxxxxxxxxxxxxxxxxxxxx"
ENV TWILIO_TOKEN="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5004
CMD python app.py
