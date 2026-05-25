FROM python:3.11-slim
WORKDIR /opt/manager
RUN pip install --no-cache-dir Flask==3.0.0 ruamel.yaml==0.18.5
COPY . .
EXPOSE 3335
CMD ["python", "/opt/manager/app.py"]