class RegExValidation:
    def __init__(self):
        pass

    def validPatt(self, reg, string):
        from re import compile
        reg = compile(reg)
        return bool(reg.match(string))

    def validPassword(self, string):
        reg = r'^[^\n\s\t\\\/]{8,}$'
        return self.validPatt(reg, string)

    def validUserId(self, string):
        reg = r'^[\w]{5,}$'
        return self.validPatt(reg, string)

    def validRecoveryhint(self, string):
        reg = r'^[\w\s]+$'
        return self.validPatt(reg, string)

    def validRegion(self, string):
        reg = r'^(nid|sid|ita|thi|chi|raj|conti|none)$'
        return self.validPatt(reg, string)

    def validBool(self, string):
        reg = r'^(True|False)$'
        return self.validPatt(reg, string)

    def validType(self, string):
        reg = r'^(sta|des|mcs|ref|bre)$'
        return self.validPatt(reg, string)

    def validFoodName(self, string):
        reg = r'^[A-Za-z0-9\s]{5,}$'
        return self.validPatt(reg, string)

    def validEmail(self, string):
        reg = r'^(([\w]+((\.|\-)[\w]+)*)|(\".+\"))@'\
              '((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|'\
              '(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        return self.validPatt(reg, string)

    def validPhone(self, string):
        reg = r'^[6-9][0-9]{9}$'
        return self.validPatt(reg, string)

    def validTable(self, string):
        reg = r'^([1-9]|[1-9]\d\d?)$'
        return self.validPatt(reg, string)

    def validName(self, string):
        reg = r'^[a-zA-Z\s]{5,}$'
        return self.validPatt(reg, string)

    def validAddress(self, string):
        reg = r'^([\sA-Za-z0-9,-]+)$'
        return self.validPatt(reg, string)

    def validPrice(self, string):
        reg = r'^[1-9]\d{,3}$'
        return self.validPatt(reg, string)


def main():
    pass


if __name__ == '__main__':
    main()
