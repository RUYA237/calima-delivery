FROM python:3.12-slim

WORKDIR /app

COPY main.py datos.py validaciones.py cliente.py empresa.py ./

CMD ["python", "main.py"]