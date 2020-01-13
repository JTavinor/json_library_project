import json


with open('library1.json', 'w') as file:
    json.dump({}, file)

with open('library1.json', 'r') as file:
    books = json.load(file)  # reads the file and turns it into a dictionary


"""
add_genre() allows the user to add a new genre to their library
if genre already exists in library, tell the user
"""


def add_genre(new_genre=None):
    if new_genre is None:
        new_genre = input('What is the name of the genre you would like to add to your library?: ').title().strip()
    match = [genre for genre in books.keys() if new_genre == genre]
    if not match:
        books[new_genre] = []
        with open("library1.json", "w") as file:
            json.dump(books, file)
            print(f'{new_genre} has been added as a genre\n')
    else:
        print(f'{new_genre} already exists in your library!\n')


"""
add_book gives the current genres in the library in a nice format and asks what genre they would like to add to
if their input exists as a genre it asks book details and adds the book to the genre
if their input does not exist as a genre it calls no_match which allows it to add the genre
If the new_entry is already in the genre, will tell user and not add book 
"""


def add_book():
    genre_format = ', '.join(books.keys())
    print(f'These are the current genres in your library: {genre_format}')
    add_to_genre = input("What genre do you want to add a book to?: ").title().strip()

    match = [genre for genre in books.keys() if add_to_genre == genre]
    if not match:
        no_match(add_to_genre)
        return

    name = input('What is the books name?: ').title().strip()
    author = input('Who is the author?: ').title().strip()
    read = input(f'Have you read {name}? (yes/no): ').lower().strip()
    while read != 'yes' and read != 'no':
        print('Input must be yes or no!')
        read = input(f'Have you read {name}? (yes/no): ')

    new_entry = {'name': name, 'author': author, 'read': read}

    for book in books[add_to_genre]:
        if book['name'] == new_entry['name'] and book['author'] == new_entry['author']:
            print(f'{name} by {author} already exists in {add_to_genre}!\n')
            return

    books[add_to_genre].append(new_entry)
    print(f'{name} by {author}, read: {read} has been added to {add_to_genre}\n')

    with open("library1.json", "w") as file:
        json.dump(books, file)


"""
If the user tries to add a book to a genre that doesn't exist in their library in add_book() it will call no_match
no_match asks whether they want to add this genre. If so it calls add_genre
If the user does not want to add the genre it will return the user to add_book
"""


def no_match(genre):
    print(f'No genre of name {genre} exists in your library!\n')
    retry = input(f'Do you want to add {genre} as a new genre (a)? Or try to add a book again (t)?: ').lower().strip()
    while retry != 'a' and retry != 't':
        print(f'{retry} is not a valid keyword please try again')
        retry = input(
            f'Do you want to add {genre} as a new genre (a)? Or try to add a book again (t)?: ').lower().strip()

    if retry == 't':
        print()
        add_book()
    elif retry == 'a':
        print()
        add_genre(genre)


"""
view_library views all books and genres in library
"""


def view_library():
    for genre in books:
        if books[genre]:
            print(f'{genre}')
        for book in books[genre]:
            for key, value in book.items():
                print(f"{key.title()} : {value.title()}")
            print()


SEARCH_OPTIONS = """Do you want to search by:
- Genre (g)
- Book title (t)
- Author(a)
- or whether you have read the book (r)
Input: """


def search_menu():
    user_input = input(SEARCH_OPTIONS).lower().strip()
    print()
    if user_input == 'g':
        genre_type = input('What genre do you want to search for?: ').title().strip()
        print()
        search_genre(genre_type)
    if user_input == 't':
        name = input('What is the name of the book you want to search for?: ').title().strip()
        print()
        search_books(name, 'name')
    if user_input == 'a':
        author = input('What is the name of the author you want to search for?: ').title().strip()
        print()
        search_books(author, 'author')
    if user_input == 'r':
        read_term = input("Do you want to see books you've read or books you haven't read (yes/no)?: ")
        print()
        search_books(read_term, 'read')


def search_genre(genre_type):
    for genre in books:
        if genre_type == genre:
            print(f'{genre_type}')
            for book in books[genre_type]:
                for key, value in book.items():
                    print(f"{key.title()} : {value.title()}")
                print()


def search_books(name, book_key):
    matches = []
    for genre in books:
        for book in books[genre]:
            if book[book_key] == name:
                matches.append(book)
                print(genre)
                for key, value in book.items():
                    print(f"{key.title()} : {value.title()}")
                print()

    if not matches:
        print(f'No book of {keyy} {name} in your library\n')


def mark_read():
    read_book = input('\nWhat is the name of the book you have read?: ').title().strip()
    read_author = input(f'Who is the author {read_book}?: ').title().strip()
    matches = []
    for genre in books:
        for book in books[genre]:
            if book['name'] == read_book and book['author'] == read_author:
                matches.append(book)
                book['read'] = 'yes'
                print(f'{read_book} by {read_author} set to read\n')
    if not matches:
        print(f'No book of name {read_book} in your library\n')

    with open("library1.json", "w") as file:
        json.dump(books, file)


def prompt_delete():
    delete_what = input('Do you want to delete a book or a genre? (b/g): ').lower().strip()
    if delete_what == 'b':
        delete_book()
    elif delete_what == 'g':
        delete_genre()
    else:
        print(f'{delete_what} is not a valid keyword!')
        prompt_delete()


def delete_book():
    book_to_del = input('What book do you want to delete?: ').title().strip()
    book_del_list = []
    for genre in books:
        for book in books[genre]:
            if book['name'] == book_to_del:
                book_del_list.append(book)

    if len(book_del_list) > 1:
        print(f'More than one book with name {book_to_del} in your library!: ')
        for book in book_del_list:
            print(f"{book['name']} by {book['author']}")
        author = input(f'\nName the author of {book_to_del} you want to delete: ').title().strip()
        book_del_list = [book for book in book_del_list if book['author'] == author]

    elif len(book_del_list) == 0:
        print(f'No book {book_to_del} in your library!\n')
        return

    else:
        for genre in books:
            for book in books[genre]:
                if book in book_del_list:
                    books[genre].remove(book)

    with open('library1.json', 'w') as file:
        json.dump(books, file)

    print(f"{book_del_list[0]['name']} by {book_del_list[0]['author']} has been deleted from your library\n")


def delete_genre():
    genre_format = ', '.join(books.keys())
    print(f'These are the current genres in your library: {genre_format}')
    genre_to_del = input('What genre do you want to delete?: ').title().strip()
    delete = [genre for genre in books if genre == genre_to_del]
    if not delete:
        print(f'No genre {genre_to_del} in your library\n')
        return
    else:
        for genre in delete:
            del books[genre]

    print(f'{genre_to_del} has been deleted from your library\n')
    with open('library1.json', 'w') as file:
        json.dump(books, file)
