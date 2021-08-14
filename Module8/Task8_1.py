from datetime import datetime, timedelta

Sasha_BD = datetime(year=1988, month=8, day=17)
Katya_BD = datetime(year=1996, month=8, day=17)
Mariana_BD = datetime(year=2019, month=8, day=19)
Robert_BD = datetime(year=2019, month=8, day=15)

users = [
    {"name": "Sasha", "birthday": Sasha_BD},
    {"name": "Katya", "birthday": Katya_BD},
    {"name": "Mariana", "birthday": Mariana_BD},
    {"name": "Robert", "birthday": Robert_BD}
]

def congratulate(users):
    final = {}
    today = datetime.now()
    w = today.weekday()
    week_end = today + timedelta(days=6-w)
    next_week_end = week_end + timedelta(days=7)
    for person in users:
        BD = datetime(year=today.year, month=person["birthday"].month, day=person["birthday"].day)
        if week_end < BD < next_week_end:
            if not BD.weekday() in final:
                final[BD.weekday()] = person["name"]
            else:
                final[BD.weekday()] += f", {person['name']}"
    WD = {
        0: "Monday",
        1: "Tuesday",
        2: "Wensday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
    }
    for n in range(7):                      # to sort final
        if n in final:
            print(f"{WD[n]}: {final[n]}")




congratulate(users)


