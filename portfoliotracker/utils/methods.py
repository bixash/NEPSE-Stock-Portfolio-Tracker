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

def stringToInt(quantity):
    
    if quantity == '-':
        quantity = 0
    else:
        quantity = int(quantity)
    return quantity

def shorten_history(history):
    history = (history.strip()).split()

    if history[0] == 'INITIAL':
        history = history[4]
    else:
        history = history[0]
    return history

def tupleToStr(tup):
    st = ''.join(map(str, tup))
    return st

def ZeroBalancetoEmpty(trans):
    for item in trans:
        for data in item:
            if data[1] == 0:
                item.remove(data)
    return trans





def convert_date_format(input_date):
    from datetime import datetime
    # Parse the input date string
    date_obj = datetime.strptime(input_date, "%Y-%m-%d")

    # Format the date in the desired format
    formatted_date = date_obj.strftime("%d %b, %Y")

    return formatted_date

