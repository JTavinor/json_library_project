import functions

"""
User menu to navigate the app, split apart to improve readability and easier to change
all other functionality is imported from the functions file
"""


MENU_PROMPT = """Do you want to:
- Add a new genre to your library (g)
- Add a new book to a genre (a)
- View your library (v)
- Search your library (s)
- Mark a book in your library as read (r)
- Delete something from your library (d)
- Quit the app (q)
Input: """

MENU_OPTIONS = {
    'g': functions.add_genre,
    'a': functions.add_book,
    'v': functions.view_library,
    's': functions.search_menu,
    'r': functions.mark_read,
    'd': functions.prompt_delete
}


def menu():
    while (user_input := input(MENU_PROMPT).lower().strip()) != "q":
        try:
            MENU_OPTIONS[user_input]()
        except KeyError:
            print("\nInvalid keyword, please try again\n")

    print('\nGoodbye!')


menu()
