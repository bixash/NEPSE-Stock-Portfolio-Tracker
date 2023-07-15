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

def allowed_file(filename):
    from .. import ALLOWED_EXTENSIONS
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

