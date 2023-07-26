import csv
import os
from collections import UserDict

from colorama import Fore, Style
from prettytable import PrettyTable

storage = "NoteBook/notes_book.csv"


class Note:
    def __init__(self, title, content, tags):
        self.title = title
        self.content = content
        self.tags = tags

    def __str__(self):
        tags_str = ", ".join(self.tags) if self.tags is not None else ""
        return f"\n{Fore.RED}Title:{Style.RESET_ALL} {self.title}\n{Fore.RED}\
Content: {Style.RESET_ALL} {self.content}\n{Fore.RED}\
Tags: {Style.RESET_ALL} {tags_str}"


class NotesBook(UserDict):
    def add_note(self, title, content, tags):
        original_title = title
        count = 1
        while title in self.data:
            title = f"{original_title} ({count})"
            count += 1
        note = Note(title, content, tags)
        self.data[title] = note

    def search_notes(self, keyword):
        found_notes = []
        for (
            note
        ) in (
            self.data.values()
        ):  # перевіряємо чи містить заголовок або вміст ключове слово keyword.
            if (
                keyword.lower() in note.title.lower()
                or keyword.lower() in note.content.lower()
            ):
                found_notes.append(note)
        if found_notes:
            table = PrettyTable()
            table.field_names = ["Title", "Content"]
            for note in found_notes:
                table.add_row([note.title, note.content])
            print(f"\n{Fore.YELLOW}Found {len(found_notes)} note(s):{Style.RESET_ALL}")
            print(table)
            print("----------------------------")
        else:
            print(f"{Fore.RED}No matching notes found.")

    def sort_notes_by_tag(self, tag):
        found_notes = []
        for note in self.data.values():
            if (
                note.tags is not None
                and isinstance(note.tags, list)
                and any(tag.lower() in t.lower() for t in note.tags)
            ):
                found_notes.append(note)
        if found_notes:
            table = PrettyTable()
            table.field_names = ["Title", "Content"]
            for note in found_notes:
                table.add_row([note.title, note.content])
            print(f"\n{Fore.YELLOW}Notes with tag '{tag}':{Style.RESET_ALL}")
            print(table)
            print("----------------------------")
        else:
            print(f"{Fore.RED}No notes found with tag '{tag}'.{Style.RESET_ALL}")

    def edit_note(self, title):
        found_note = self.data.get(title)

        if found_note:
            new_content = input("Enter new content for the note: ")
            found_note.content = new_content
            print(f"{Fore.GREEN}Note updated successfully!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Note not found.{Style.RESET_ALL}")

    def delete_note(self, title):
        if title in self.data:
            del self.data[title]
            print(f"{Fore.GREEN}Note deleted successfully!{Style.RESET_ALL}")
        else:
            for key in self.data.keys():
                if key.lower().strip() == title.lower().strip():
                    del self.data[key]
                    print(f"{Fore.GREEN}Note deleted successfully!{Style.RESET_ALL}")
                    return
            print(f"{Fore.RED}Note not found.{Style.RESET_ALL}")

    def display_all_notes(self, notes_per_page):
        if self.data:
            total_notes = len(self.data)
            total_pages = (total_notes + notes_per_page - 1) // notes_per_page
            current_page = 1
            while True:
                print(
                    f"\n{Fore.YELLOW}Page {current_page} of {total_pages}:{Style.RESET_ALL}"
                )
                notes_to_display = list(self.data.values())[
                    (current_page - 1) * notes_per_page : current_page * notes_per_page
                ]
                if notes_to_display:
                    table = PrettyTable()
                    table.field_names = ["Title", "Content", "Tags"]
                    for note in notes_to_display:
                        table.add_row(
                            [
                                note.title,
                                note.content,
                                ", ".join(note.tags) if note.tags else "-",
                            ]
                        )
                    print(table)
                else:
                    print(f"{Fore.RED}No notes found on this page.{Style.RESET_ALL}")

                if current_page < total_pages:
                    choice = input(
                        f"Press 'Enter' to view the next page, or 'q' to quit: "
                    )
                    if choice.lower() == "q":
                        break
                    current_page += 1
                else:
                    print("End of notes.")
                    break
        else:
            print(f"{Fore.RED}No notes found.{Style.RESET_ALL}")


if __name__ == "__main__":
    notebook = NotesBook()

    if os.path.isfile(storage):
        with open(storage, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                title = row[0]
                content = row[1]
                tags = row[2].split(",") if row[2] else None
                notebook.add_note(title, content, tags)

while True:
    menu_table = PrettyTable()
    menu_table.field_names = ["Option", "Description"]
    menu_table.add_row(["1", "Add a note"])
    menu_table.add_row(["2", "Search notes"])
    menu_table.add_row(["3", "Sort notes by tag"])
    menu_table.add_row(["4", "Edit a note"])
    menu_table.add_row(["5", "Delete a note"])
    menu_table.add_row(["6", "Display all notes"])
    menu_table.add_row(["7", "Exit"])
    print(menu_table)
    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        title = input("Enter note title: ")
        content = input("Enter note content: ")
        tags = input("Enter comma-separated tags: ").split(",")
        notebook.add_note(title, content, tags)
        print(f"{Fore.GREEN}Note added successfully!{Style.RESET_ALL}")
    elif choice == "2":
        keyword = input("Enter a keyword to search notes: ")
        notebook.search_notes(keyword)
    elif choice == "3":
        tag = input("Enter a tag to sort notes: ")
        notebook.sort_notes_by_tag(tag)
    elif choice == "4":
        title = input("Enter the title of the note to edit: ")
        notebook.edit_note(title)
    elif choice == "5":
        title = input("Enter the title of the note to delete: ")
        notebook.delete_note(title)
    elif choice == "6":
        notes_per_page = 3
        notebook.display_all_notes(notes_per_page)
    elif choice == "7":
        # print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")

    with open(storage, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Content", "Tags"])
        for record in notebook.data.values():
            title = record.title
            content = record.content
            tags = ",".join(record.tags) if record.tags else ""
            writer.writerow([title, content, tags])
