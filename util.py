from datetime import datetime

def smart_semester():
    month = datetime.today().month
    if month > 5:
        return 2
    else:
        return 1

def smart_year():
    return str(datetime.today().year)