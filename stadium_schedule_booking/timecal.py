def timecal(slots):
    if len(slots)==0:
        return []

    start = [slots[0]]
    end = []
    ed = -1
    flag = False
    for i in range(len(slots) - 1):
        if ed == -1:
            st = slots[i]
            ed = slots[i]
        if slots[i] + 1 == slots[i + 1]:
            ed = slots[i + 1]
        else:
            end.append(slots[i] + 1)
            start.append(slots[i + 1])
            ed = -1

    if slots[-1] == ed:
        end.append(slots[-1] + 1)
    if len(end) == 0:
        flag = True
        end.append(slots[-1])
    print(start)
    print(end)

    bookings = []

    if not flag:
        for i in range(len(end)):
            bookings.append(f"{start[i]} - {end[i]}")
        # bookings.append(f"{start[len(start)-1]} - {start[len(start)-1]+1}")
    else:
        for i in range(len(end)):
            bookings.append(f"{start[i]} - {end[i] + 1}")
    print(bookings)

