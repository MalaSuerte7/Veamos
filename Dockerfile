FROM python:3-slim
WORKDIR /programas/entrenadores
RUN pip3 install fastapi uvicorn pydantic mysql-connector-python
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]