from datetime import datetime, timedelta


def get_week(check_date=datetime.now(), init_date=datetime(2017,9,12,6)):
    a_week = timedelta(weeks=1)
    date_list = []
    potential_weeks = []

    # generate regular season & playoff weeks
    for ii in range(0,20):
        date_list.append((ii+1, init_date + a_week * ii))
    # include Superbowl week
        date_list.append((22, init_date + a_week * 22))

    # find min of weeks
    for week in date_list:
        if check_date < week[1] :
            potential_weeks.append(week[0])
    return min(potential_weeks)


if __name__ == '__main__':
    get_week()
