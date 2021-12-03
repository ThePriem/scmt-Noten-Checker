import schedule
import time
from main import hourlyUpdate
from datetime import datetime

def main():
    schedule.every(1).hour.at(":05").do(hourlyUpdate)

    difMinutesOld = None

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
