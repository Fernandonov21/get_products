# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5003)  # Asigna el puerto específico para el microservicio "read"
