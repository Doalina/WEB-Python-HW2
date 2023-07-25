import re
from collections import UserDict
from datetime import datetime


class GoofyIterator:
    def __init__(self, data, N):
        self.N = N
        self.data = data
        self.max_records = len(self.data)
        self.max_pages = (
            (self.max_records // self.N) + 1
            if (self.max_records % self.N)
            else self.max_records // self.N
        )
        self.current_start = 0
        self.current_end = self.N if self.N <= self.max_records else self.max_records
        self.page_counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.page_counter >= self.max_pages:
            raise StopIteration
        else:
            result = ""
            records = list(self.data.items())
            for i, j in records[self.current_start : self.current_end]:
                if j.bday and j.bday.value:
                    result += f'{i}:{", ".join(k.value for k in j.phones)}, and birthday is {j.bday.value}!\n'
                else:
                    result += f'{i}:{", ".join(k.value for k in j.phones)}\n'

            self.current_start = self.current_end
            self.current_end = min(self.current_end + self.N, self.max_records)
            self.page_counter += 1

            result += "\n"
            return result


class AddressBook(UserDict):
    """A class representing an address book, which contains a collection of Record objects."""

    def add_record(self, record):
        """Add a record to the address book."""
        self.data[record.name.value] = record
        return "successfully added"

    def delete_record(self, record):
        """Delete a contact in the address book."""
        del self.data[record.name.value]
        return "successfully removed"

    def iterator(self, N=10):
        return GoofyIterator(self.data, N)


class Record:
    """A class representing a record in an address book."""

    def __init__(self, name, phones, bday=None):
        self.name = name
        self.phones = phones
        self.bday = bday

    def add_phones(self, phones):
        self.phones += phones
        return "successfully added"

    def add_bday(self, bday):
        self.bday = bday
        return "successfully added"

    def change_phones(self, phones):
        self.phones = phones
        return "successfully changed"

    def change_bday(self, bday):
        self.bday = bday
        return "successfully changed"

    def days_to_birthday(self):
        if not self.bday:
            return "no birthday recorded yet for this contact!"
        if not self.bday.value:
            return "no birthday recorded yet for this contact!"

        else:
            bday = self.bday.value.strip()
            today = datetime.today().date()
            try:
                target_date = (
                    datetime.strptime(bday, "%d/%m").date().replace(year=today.year)
                )
                if target_date < today:
                    target_date = (
                        datetime.strptime(bday, "%d/%m")
                        .date()
                        .replace(year=today.year + 1)
                    )
            except:
                target_date = (
                    datetime.strptime(bday, "%d/%m/%Y").date().replace(year=today.year)
                )
                if target_date <= today:
                    target_date = (
                        datetime.strptime(bday, "%d/%m/%Y")
                        .date()
                        .replace(year=today.year + 1)
                    )

        return (
            f"{(target_date - today).days} days left to {self.name.value}'s Birthday!"
        )


class Field:
    """A class representing a generic field."""

    def __init__(self, value):
        self.value = value


class Name(Field):
    """idk what's specific about this field, let it be random but limited in length"""

    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if 0 < len(new_value) <= 15:
            self.__value = new_value
        else:
            raise ValueError(
                "Exceeded length of the name! Please remove the cat from the keyboard"
            )


class Phone(Field):
    """phones must only contain digits or special charecters!"""

    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if 0 < len(new_value) <= 15 and re.search(r"^[0-9\s_+]+$", new_value):
            self.__value = new_value
        else:
            raise ValueError(
                "Phones must only contain digits or +, and be no  longer than 15 sympols!"
            )


class Birthday(Field):
    """dd/mm or --dd/mm/yyyy"""

    def __init__(self):
        self.__value = None

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if re.search(r"\s?\d{2}/\d{2}(/\d{4}})?\s?", new_value):
            self.__value = new_value
        else:
            raise ValueError(
                "Oops! birthday format is incorrect for this feature. Type add name --dd/mm or --dd/mm/yyyy"
            )
