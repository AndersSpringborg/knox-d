import random

def random_percentage_count():
    """
    This is gimmick percentages for fun loading experience!!!
    """
    var = "%"
    listofnumbers = random.sample(range(0, 99), 5)
    listofnumbers.sort()

    for number in listofnumbers:
        print(number, var, sep='')
    print("100%")
