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

transactions = [[('MKHC', 10, 255)], [('NABIL', 1, 590.1)], [('SANIMA', 2, 247.1)], [('NTC', 0, 870)], [('NICA', 0, 750)], [('PCBL', 1, 192.4)], [('ADBL', 0, 229)], [('NIFRA', 0, 234.5)], [('AVYAN', 0, 650)], [('UHEWA', 0, 346)], [('RFPL', 0, 271.4)], [('MBJC', 0, 338)], [('PLI', 0, 560)], [('NYADI', 0, 285)], [('ULI', 0, 393.8)], [], [('NICSF', 100, 8.37)]]

def notListed(transactions):
    for item in transactions:
        if not item:
            transactions.remove(item)
    return transactions

def removeBalance(trans):
    for item in trans:
        for data in item:
            if data[1] == 0:
                item.remove(data)
    return trans


temp = notListed(transactions)
print(temp)
print("\n\n\n")
list = removeBalance(temp) 
print(list) 
print("\n\n\n")
new = notListed(temp)
print(new)
