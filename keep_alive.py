from flask import Flask
from threading import Thread
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask('')

@app.route('/')
def home():
    return "EmailBot is running"

sched = BackgroundScheduler(daemon=True)
sched.start()

def run():
  app.run(host='0.0.0.0',port=9090)

def keep_alive():  
    t = Thread(target=run)
    t.start()