def validPatt(reg, string):
    from re import compile
    reg = compile(reg)
    return bool(reg.match(string))


def validPassword(string):
    reg = r'^[^\n\s\t\\\/]{8,}$'
    return validPatt(reg, string)


def validUserId(string):
    reg = r'^[\w]{5,}$'
    return validPatt(reg, string)


def validRecoveryhint(string):
    reg = r'^[\w\s]+$'
    return validPatt(reg, string)


def validEmail(string):
    reg = r'^(([\w]+((\.|\-)[\w]+)*)|(\".+\"))@'\
          '((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|'\
          '(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    return validPatt(reg, string)


def validPhone(string):
    reg = r'^[6-9][0-9]{9}$'
    return validPatt(reg, string)


def validName(string):
    reg = r'^[a-zA-Z\s]{5,}$'
    return validPatt(reg, string)


def validAddress(string):
    reg = r'^([\sA-Za-z0-9,-]+)$'
    return validPatt(reg, string)


def main():
    print(validName('rahul sahu'))
    print(validEmail('rahulsahu9719.@gamil.com'))
    print(validAddress('C-119, KP-9, KIIT University, Bhubaneshwar'))


if __name__ == '__main__':
    main()
