from dotenv import load_dotenv
load_dotenv()

# main.py
from ui import VirtualLabApp

if __name__ == "__main__":
    app = VirtualLabApp()
    app.run()
