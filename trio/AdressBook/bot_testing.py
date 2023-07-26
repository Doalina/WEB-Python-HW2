import pickle

from bot import *
from my_classes import *
from parser_oop import Command
from search import bday_people, search


# Main loop but iterating over tests.txt, not the console input
@input_error
def main():
    """Main function that runs the program."""
    with open("AdressBook/tests.txt", "r") as fh:
        for cmd in fh.readlines():
            print("> " + cmd.strip())
            user_input = cmd.strip()

            if user_input in BREAK_POINTS:
                break

            c = Command(user_input)
            if c.command == "add":
                if c.name:
                    result = add(c.name, c.phones, bday=c.bday)
                    print(result)
                else:
                    print("name required!")
            elif c.command == "change":
                result = change(c.name, c.phones, bday=c.bday)
                print(result)

            elif c.command == "page":
                it = DATA.iterator(number_of_cntacts_on_page)
                while True:
                    inp = input(
                        'type "b" to stop scrolling and go back, press enter to see the next page\n'
                    ).strip()
                    if inp == "b":
                        break
                    elif it.page_counter >= it.max_pages:
                        print("the end!")
                        break

                    page = next(it)
                    print(page)

            elif c.command == "search":
                while True:
                    pattern = input(
                        'please specify your search pattern or enter "b" to quit search: '
                    )
                    if pattern.strip() == "b":
                        break
                    else:
                        print(search(pattern, DATA))

            elif re.search(r"bdays \d+", user_input):
                print(bday_people(DATA, re.search(r"\d+", user_input).group()))

            else:
                command, *data = c.command, c.name, c.phones
                if func := commands.get(command):
                    print(func(*data))

                else:
                    print(
                        "No such command! To see available list of commands type 'help' "
                    )

    print("Good bye!")


if __name__ == "__main__":
    main()
    with open(storage_name, "wb") as fh:
        pickle.dump(DATA, fh)
