from datetime import datetime, timedelta


def get_week(check_date=datetime.now(), init_date=datetime(2018, 9, 4, 6)):
    """
    Returns the week of the season
    :param check_date:
    :param init_date:
    :return:
    """
    a_week = timedelta(weeks=1)
    date_list = []
    potential_weeks = []

    # generate regular season & playoff weeks as tuples: (week, date)
    for ii in range(0,20):
        date_list.append((ii+1, init_date + a_week * ii))
    # include Superbowl week
    date_list.append((22, init_date + a_week * 22))

    # find min of week, for dates in the future
    for week_date in date_list:
        if check_date < week_date[1]:
            potential_weeks.append(week_date[0])

    return min(potential_weeks)


if __name__ == '__main__':
    print(get_week())
