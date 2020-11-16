import random

def random_percentage_count():
    """
    This is gimmick percentages for fun loading experience!!!
    """
    var = "%"
    forloopnumber = random.randint(1,10)
    listofnumbers = random.sample(range(0, 99), forloopnumber)
    if 69 not in listofnumbers:
        listofnumbers.append(69)
    listofnumbers.sort()

    for number in listofnumbers:
        print(number, var, sep='')
    if listofnumbers[0] < 5:
        print("420%")
    else:
        print("100%")
