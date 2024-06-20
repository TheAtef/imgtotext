from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def ping():
    return "Ligma!"

def run():
  app.run(host='0.0.0.0',port=8080)

def server():
    t = Thread(target=run)
    t.start()