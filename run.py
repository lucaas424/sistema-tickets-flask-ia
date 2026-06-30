from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app()

if __name__ == "__main__":
    print("Iniciando TicketFlow IA...")
    print("Abrí en el navegador: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)