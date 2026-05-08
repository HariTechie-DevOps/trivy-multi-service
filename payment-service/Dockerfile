FROM python:3.9-slim
USER root
ENV STRIPE_KEY="sk_live_4eC39HqLyjWDarjtT1zdp7dc"
ENV DB_PASSWORD="admin123"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5002
CMD python app.py
