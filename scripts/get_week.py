from datetime import datetime, date, timedelta

def GetWeek(check_date = datetime.now(), initDate = datetime(2017,9,12,6)):
    aWeek = timedelta(days = 7)
    myList = []
    potential_weeks = []
    for ii in range(0,20):
        myList.append((ii+1, initDate + aWeek * ii))
    myList.append((22, initDate + aWeek * 22))
    for week in myList:
        if check_date < week[1] :
            potential_weeks.append(week[0])
    return min(potential_weeks)

GetWeek()
