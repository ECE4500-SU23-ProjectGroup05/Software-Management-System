import time


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def sleep_for_some_time(hours=72):
    print("The thread will sleep for " + str(hours) + " hours.")
    time.sleep(hours * 3600)
