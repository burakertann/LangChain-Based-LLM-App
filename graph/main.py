from dotenv import load_dotenv
from graph.graph import app
#python -m graph.main
load_dotenv()

if __name__ == "__main__":
    print(app.invoke(input = {"question" : "what is the current weather in Istanbul"}))