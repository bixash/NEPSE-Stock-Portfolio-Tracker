def toDoubleDigit(date):
    if int(date) < 10:
        date = '0'+ date
    return date

def date_format(date):
    newDate = date.split("/")
   
    month = toDoubleDigit(newDate[0])
    day = toDoubleDigit(newDate[1])
    year = newDate[2]

    newDate[0] = year
    newDate[1] = month
    newDate[2] = day

    newDate = "-".join(newDate)

    return newDate