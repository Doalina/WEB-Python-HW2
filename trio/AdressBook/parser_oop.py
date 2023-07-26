# command parser oop
# it was easier to test the code and I read about the encapsulation setter/getter trick only later!!
# I now realize it would be even better to make a field check while parsing the input
# in Command() once and for good, but homework wants otherwise
import re

# not including breaking points
commands_list = [
    "hello",
    "add",
    "change",
    "call",
    "delete",
    "remove",
    "show_all",
    "help",
    "bday",
    "page",
    "search",
]

commands_pattern = "|".join(commands_list)  # hello|add|.... needed for further regex

# typical command example:
ex1 = "add ann ros  -150 -156  --9/33/1098 "  # command on the start, name, -number(s)(optional), --bday(optional)

input_regex = rf"^({commands_pattern})(.*?)(?: (-[^-]+)*)?(?: (--[^-]+)?)?$"  # (command)(name)(numbers(s))(bday)


class Command:
    def __init__(self, input_string):
        match = re.search(input_regex, input_string)
        if match:
            self.raw = input_string  # match.group(0)
            self.command = match.group(1)
            self.name = match.group(2).lstrip()
            self.phones = re.findall(r"\s-((?!-)\S+)", input_string)
            # here I need a list rather then a single match.group(3)
            self.bday = match.group(4)
        else:
            self.raw = None
            self.command = None
            self.name = None
            self.phones = None
            self.bday = None
        if self.bday:
            self.bday = self.bday.strip("--")


# c = Command(ex1)
# print(c.raw)
# print(c.command)
# print(c.name)
# print(c.phones)
# print(c.bday)
