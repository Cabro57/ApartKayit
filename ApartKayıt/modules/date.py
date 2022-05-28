from datetime import date
from datetime import datetime
from datetime import timedelta
import locale

locale.setlocale(locale.LC_ALL, "")


def takeDate(day, month, year):
    date = datetime(year, month, day)
    time_stamp = datetime.timestamp(date)
    return time_stamp


def giveDate(stamp,param):
    from_time = date.fromtimestamp(stamp)
    if param == "bool":
        if from_time == date.today():
            return True
        else:
            return False
    elif param == "string":
        if from_time == date.today():
            return "{} (Bugün)".format(date.strftime(from_time, "%d %B %A"))
        else:
            return date.strftime(from_time, "%d %B %A")
    elif param == "date":
        return from_time

    else:
        pass

def calculate(entry,exit):
    if entry > exit:
        return False
    else:
        return True


def today():
    return date.today()


"""def calculate(entry, exit):
    t1 = timedelta(seconds= takeDate(exit))
    t2 = timedelta(seconds= takeDate(entry))
    return t1 - t2"""



"""
tarih = datetime.now()
print(tarih)
zaman_damgasi = datetime.timestamp(tarih)

print(zaman_damgasi)

tarih = tarih.strftime("%d")
print(tarih)
"""
