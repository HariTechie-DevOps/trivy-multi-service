FROM python:3.9-slim
USER root
ENV SECRET_KEY="hardcoded-secret"
ENV JWT_SECRET="never-share-this-key"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5001
CMD python app.py
