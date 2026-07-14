import schedule
import time
import os

def run_pipeline():
    print("Collecting Crypto Data...")
    os.system("python -m pipeline.load_mysql")

schedule.every(5).minutes.do(run_pipeline)

print("Scheduler Started...")

while True:
    schedule.run_pending()
    time.sleep(1)