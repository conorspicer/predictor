from datetime import datetime, date, timedelta
def get_week(check_date = datetime.now(), initDate = datetime(2017,9,13)):
    aWeek = timedelta(days = 7)
    myList = []
    for ii in range(0,17):
        myList.append(('WK'+str(ii+1), initDate + aWeek * ii))
    myList.append(('WILDCARD', initDate + aWeek * 18))
    myList.append(('DIVISIONAL', initDate + aWeek * 19))
    myList.append(('CHAMPIONSHIP', initDate + aWeek * 20))
    myList.append(('SUPERBOWL', initDate + aWeek * 22))
    for week in myList:
        if check_date < week[1] :
            return(week[0])
        else:
            return 'SUPERBOWL'
