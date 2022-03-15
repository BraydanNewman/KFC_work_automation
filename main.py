import scraper
import time

if __name__ == '__main__':
    updater = scraper.ScheduleUpdate()

    for i in range(6):
        updater.login()
        if updater.success:
            print("Can not login")
            break
        time.sleep(5)
        if i > 5:
            updater.driver_exit()
            print("Failed to Access data")
            break
        if updater.success:
            updater.extract_schedule()
        else:
            print("Failed to Access data")
            break
        if updater.success:
            updater.get_events()
            updater.input_to_calender()
            print("Completed inputting shifts into calender")
        else:
            print("Failed to Access data")



