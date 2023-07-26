# AdressBook().data= {str:Record(),}
# Record() .name | .phones | .bday
# phones=[Phone(Field),]
# Field() .value #last stop

from datetime import datetime, timedelta


def search(what, where):
    results = []
    # for name, record in AdressBook().data.items()
    for name, record in where.data.items():
        record_text = f'{name}:{", ".join(ph.value for ph in record.phones)};'
        if record.bday:
            record_text = f'{name}:{", ".join(ph.value for ph in record.phones)}; {record.bday.value}'
        if what.lower() in record_text.lower():
            results.append(record_text)
    if results == []:
        return 'no match! type "search" again and try another pattern'
    return "\n".join(results)


def bday_people(book, dayz):
    results = []
    # for name, record in AdressBook().data.items()
    for name, record in book.data.items():
        if record.bday:
            today = datetime.today().date()
            try:
                bday = datetime.strptime(record.bday.value, "%d/%m")
            except:
                bday = datetime.strptime(record.bday.value, "%d/%m/%Y")
            if (today + timedelta(days=int(dayz))).strftime("%d/%m") == bday.strftime(
                "%d/%m"
            ):
                record_text = f'{name}:{", ".join(ph.value for ph in record.phones)}; {record.bday.value}'
                results.append(record_text)

    if results == []:
        return "no match!"
    return (
        "\n".join(results) + f"\nthese contacts have bday in {dayz} days this year!\n"
    )
