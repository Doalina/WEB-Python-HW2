## TRIO v.1.0.1

### how to use?

0. Make sure you have python and pip installed (python3 for mac)
1. Download the repository 
2. Launch `pip install -e /path/to/folder/trio/here` in terminal (`\path\to\folder\trio\here` for mac or linux)
3. Сall `trio` in terminal at any place
4. Enjoy!

### what does it do?

The bot has 3 main functions
1. Adress Book
    - a contact consists of a name, an arbitrary amount of phones, and a birthday
    - gives a list of employees who have a Birthday in a given amount of days
    - gives the number of days left to the birthday for a given name
    - allows search 
    - the employee data is safely stored as `data.bin` in the AdressBook folder

2. Folder Sorter
    - sorts files into separate folders with respect to the extensions;
    - renames everything with respect to the convention;
    - unpacks archives;
    - deletes empty folders;
    - ignores unknown formats;
    - sorts files in the specified folder by category: images, documents, videos;

3. Note Book 
    - a note consists of a name, content, and hashtags
    - allows search
    - allows sorting by hashtags
    - the data is conveniently stored as `notes_book.csv` in the NoteBook folder

