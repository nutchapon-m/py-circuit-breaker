import schedule
import time

def job():
    print("job complete.")

schedule.every(10).seconds.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)