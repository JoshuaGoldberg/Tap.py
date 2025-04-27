number_titles = ["Million", "Billion", "Trillion",
                 "Quadrillion", "Quintillion", "Sextillion",
                 "Septillion", "Octillion", "Nonillion",
                 "Decillion", "Undecillion", "Duodecillion",
                 "Tredecillion", "Quattuordecillion",
                 "Quindecillion", "Sexdecillion",
                 "Septdecillion", "Octodecillion",
                 "Novemdecillion", "Vigintillion"]


def format_number(number):
    if number > 999999:
        return format_number_helper(number / 1000000, 0)
    else:
        return str(number)


def format_number_helper(number, acc):
    if number >= 1000:
        return format_number_helper(number / 1000, acc + 1)
    else:
        return str(round(number, 3)) + " " + number_titles[acc]
