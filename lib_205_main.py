import pyodbc
import datetime
import getpass
import os
import colorama
from colorama import init, Fore, Back, Style

# initiation colorama in window env
init()
# os.system('cls')
title_format = '{title:^172}'

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-MIEL300\SQLEXPRESS;'
                      'Database=Lib_205;'
                      'Trusted_Connection=yes;')


def create_user_account():
    cursor_users = conn.cursor()
    insert_user_query = '''INSERT INTO Borrowers(FirstName, LastName, Password, Email, Payment, FavoriteGenre)
                                  VALUES (?,?,?,?,?,?);'''
    # get user inputs
    print(title_format.format(title='ENTER THESE INFORMATION BELOW TO REGISTER'))
    print()
    first_name = input('Enter your first name: ')
    last_name = input('Enter your last name: ')
    l_password = getpass.getpass('Enter your password: ')
    retype_password = getpass.getpass('Re-type your password: ')
    while l_password != retype_password:
        print('Your password miss match!')
        l_password = input('Enter your password: ')
        retype_password = input('Re-type your password: ')
    l_email = input('Enter your email: ')
    payment = 0
    favorite_genre = input('Enter your favorite genre: ')

    # insert into table Lib_user
    cursor_users.execute(insert_user_query, first_name, last_name, l_password, l_email, payment, favorite_genre)
    print()
    print()
    print('You register successfully, Welcome to 205 Library')
    # confirm the insert
    cursor_users.commit()
    # close the connections
    cursor_users.close()

    return 1


def get_borrower(l_email, l_password):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=DESKTOP-MIEL300\SQLEXPRESS;'
                          'Database=Lib_205;'
                          'Trusted_Connection=yes;')
    cursor_borrower = conn.cursor()

    select_borrower_query = '''SELECT * FROM Borrowers
                      WHERE Email = ? and Password = ? '''

    cursor_borrower.execute(select_borrower_query, l_email, l_password)

    l_borrower = Borrower()
    if l_borrower is not None:
        for row in cursor_borrower:
            l_borrower.id = row[0]
            l_borrower.first_name = row[1]
            l_borrower.last_name = row[2]
            l_borrower.password = row[3]
            l_borrower.email = row[4]
            l_borrower.payment = row[5]
            l_borrower.favorite_genre = row[6]
        return l_borrower
    return l_borrower


def get_librarian(l_email, l_password):
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=DESKTOP-MIEL300\SQLEXPRESS;'
                          'Database=Lib_205;'
                          'Trusted_Connection=yes;')
    cursor_librarian = conn.cursor()
    select_librarian_query = '''SELECT * FROM Librarians
                          WHERE Email = ? and Password = ? '''

    cursor_librarian.execute(select_librarian_query, l_email, l_password)
    l_librarian = Librarian()
    if l_librarian is not None:
        for row in cursor_librarian:
            for column in range(len(row)):
                l_librarian.id = row[0]
                l_librarian.first_name = row[1]
                l_librarian.last_name = row[2]
                l_librarian.password = row[3]
                l_librarian.email = row[4]
        return l_librarian

    return l_librarian


class Users:
    def __init__(self):
        self.id = -1
        self.first_name = ''
        self.last_name = ''
        self.password = ''
        self.email = ''

    def print_empty_line(self, l_number_of_lines):
        for i in range(l_number_of_lines):
            print()

    def welcome_screen(self, l_first_name, l_last_name, motd):
        format_string = '{tile:*^172}'
        print(Fore.BLUE + '=*=' * 57)
        print(Fore.RED + format_string.format(tile=l_first_name.upper() + ' ' + l_last_name.upper()))
        print(Fore.RED + format_string.format(tile=motd.upper()))
        print(Fore.BLUE + '=*=' * 57)
        print(Fore.WHITE)

    def list_books(self, l_borrower_id=0):
        list_books_query = '''Select BookID, BookName, Author, Genre from books
                            where BorrowerID = ?'''
        cursor_book = conn.cursor()
        list_books = cursor_book.execute(list_books_query, l_borrower_id)
        a_book = Books()
        format_string = '{column0:^43}{column1:^43}{column2:^43}{column3:^43}'
        print(Fore.WHITE + format_string.format(column0='Book ID'.upper(), column1='Book name'.upper(),
                                                column2='Author'.upper(),
                                                column3='Genre'.upper()))
        for row in list_books:
            a_book.book_id = row[0]
            a_book.book_name = row[1]
            a_book.author = row[2]
            a_book.genre = row[3]
            print(Fore.WHITE + format_string.format(column0=a_book.book_id, column1=a_book.book_name,
                                                    column2=a_book.author,
                                                    column3=a_book.genre))
        cursor_book.close()

    def get_late_books(self, l_borrower_id=0):
        # need to be fix
        cursor_book = conn.cursor()

        get_late_books_query = '''SELECT * FROM Books
                                  WHERE BorrowerID = ?'''
        cursor_book.execute(get_late_books_query, l_borrower_id)
        list_books = []
        i = 0
        for row in cursor_book:
            list_books.append(Books())
            list_books[i].book_id = row[0]
            list_books[i].book_name = row[1]
            list_books[i].author = row[2]
            list_books[i].genre = row[3]
            list_books[i].borrow_date = row[5]
            list_books[i].late_fee = row[4]
            list_books[i].lost = row[6]
            list_books[i].borrower_id = row[7]
            i += 1
        cursor_book.close()
        late_payment = 0
        format_string = '{column0:^34}{column1:^34}{column2:^34}{column3:^34}{column4:^34}'
        print(format_string.format(column0='Book ID', column1='Book name', column2='Author', column3='Genre',
                                   column4='Late fee'))
        for row in range(len(list_books)):
            if list_books[row].borrow_date + datetime.timedelta(days=30) < datetime.date.today():
                print(format_string.format(column0=list_books[row].book_id, column1=list_books[row].book_name,
                                           column2=list_books[row].author,
                                           column3=list_books[row].genre, column4=list_books[row].late_fee))
                late_payment += list_books[row].late_fee
        if late_payment == 0:
            print()
            print(Fore.BLUE + title_format.format(title='No book is late'))
            print(Fore.WHITE)
        else:
            print()
            print(title_format.format(title='Total late fee is: ' + Fore.RED + str(late_payment) + '$'))
            print(Fore.WHITE)


class Librarian(Users):
    def __init__(self):
        Users.__init__(self)

    def create_librarians(self):
        cursor_librarian = conn.cursor()
        create_new_librarian_query = '''INSERT INTO Librarians (Firstname, Lastname, password, email)
                                        VALUES (?, ?, ?, ?)'''
        l_firstname = input('Enter your first name: ')
        l_lastname = input('Enter your last name: ')
        l_email = input('Enter your email: ')
        l_password_1 = getpass.getpass('Enter your password: ')
        l_password_2 = getpass.getpass('Retype your password: ')

        while l_password_1 != l_password_2:
            print('Your password is miss match!!!!')
            l_password_1 = getpass.getpass('Enter your password: ')
            l_password_2 = getpass.getpass('Retype your password: ')

        cursor_librarian.execute(create_new_librarian_query, l_firstname, l_lastname, l_password_1, l_email)
        cursor_librarian.commit()
        cursor_librarian.close()

    def delete_books(self):
        name_or_id = input('Enter book\'s name or book\'s ID to delete: ')
        delete_book_query = '''DELETE FROM Books
                                WHERE BookID = ? OR BookName = ?'''
        cursor_book = conn.cursor()
        cursor_book.execute(delete_book_query, name_or_id, name_or_id)
        cursor_book.commit()
        cursor_book.close()
        print()
        print('{} is deleted'.format(name_or_id))

    def get_lost_books(self):
        pass

    def create_book(self):
        cursor_books = conn.cursor()
        insert_book_query = '''INSERT INTO Books (BookName, Author, Genre, LateFee, BorrowDate, BorrowerID)
                                VALUES (?,?,?,?,?,?);'''
        # book_id = input('Enter book ID: ')
        book_name = input('Enter book name: ')
        author = input('Enter author name: ')
        genre = input('Enter book genre: ')
        late_fee = input('Enter late return fee: ')
        borrow_date = datetime.date.today()
        # New book ID will be 0 which is belong to SYSTEM USER
        borrower_id = 0
        cursor_books.execute(insert_book_query, book_name, author, genre, late_fee,
                             borrow_date, borrower_id)
        cursor_books.commit()
        cursor_books.close()
        return 1

    def payment(self):
        l_borrower_id_email = input('Enter user\'s ID/Email address  to process: ')
        cursor_borrower = conn.cursor()
        get_payment_query = '''SELECT Payment
                                FROM Borrowers
                                WHERE BorrowerID = ? OR Email = ?'''
        cursor_borrower.execute(get_payment_query, l_borrower_id_email, l_borrower_id_email)
        current_payment = 0
        for row in cursor_borrower:
            current_payment = int(row[0])

        self.print_empty_line(1)
        amount_payment = int(input('Payment:  '))
        new_payment = current_payment - amount_payment

        update_new_payment_query = '''UPDATE Borrowers
                                        SET Payment = ?
                                        WHERE BorrowerID = ? OR Email = ?'''
        cursor_borrower.execute(update_new_payment_query, new_payment, l_borrower_id_email, l_borrower_id_email)
        cursor_borrower.commit()
        print('Payment successes!')
        print('New payment of User ID/Email: {} is: {}$ '.format(l_borrower_id_email, new_payment))
        cursor_borrower.close()

    def get_lost_books(self):
        get_lost_books_query = '''SELECT * 
                                  FROM Books
                                  WHERE BorrowerID = -1'''
        list_books = []
        cursor_book = conn.cursor()
        cursor_book.execute(get_lost_books_query)
        i = 0
        for row in cursor_book:
            list_books.append(Books())
            list_books[i].book_id = row[0]
            list_books[i].book_name = row[1]
            list_books[i].author = row[2]
            list_books[i].genre = row[3]
            list_books[i].borrow_date = row[5]
            list_books[i].late_fee = float(row[4])
            list_books[i].lost = row[6]
            list_books[i].borrower_id = row[7]
            i += 1
        cursor_book.close()
        lost_payment = 0
        format_string = '{column0:^34}{column1:^34}{column2:^34}{column3:^34}{column4:^34}'
        print(title_format.format(title='LOST BOOKS LIST'))
        print(format_string.format(column0='BOOK ID', column1='BOOK NAME', column2='AUTHOR', column3='GENRE',
                                   column4='LOST FEE'))
        for row in range(len(list_books)):
            print(format_string.format(column0=list_books[row].book_id, column1=list_books[row].book_name,
                                       column2=list_books[row].author,  # lost payment equals late fee * 3
                                       column3=list_books[row].genre, column4=list_books[row].late_fee * 3))
            lost_payment += list_books[row].late_fee * 3
        print()
        if lost_payment == 0:
            print()
            print(Fore.BLUE + title_format.format(title='No book is reported lost'))
            print(Fore.WHITE)
        else:
            print()
            print(Fore.RED + title_format.format(title='Total lost fee has to collect is: ' + str(lost_payment) + '$'))
            print(Fore.WHITE)


class Borrower(Users):
    def __init__(self):
        Users.__init__(self)
        self.payment = 0
        self.favorite_genre = ''

    def inform_charge_fee(self):
        pass

    def borrow_books(self, l_borrower_id):
        #step 1
        book_id = input('Enter book\'s ID to borrow:')
        get_book_info_query = '''SELECT * FROM Books
                                WHERE BookID = ?'''

        update_book_query = '''UPDATE Books
                                SET BorrowerID = ?, BorrowDate = ?
                                WHERE BookID = ?'''
        today = str(datetime.datetime.today())
        # create a cursor point to database(205_lib)
        cursor_book = conn.cursor()
        # run query to get book's info, step 2
        cursor_book.execute(get_book_info_query, book_id)

        # transfer book information into book object
        a_book = Books()
        for row in cursor_book:
            a_book.book_id = row[0]
            a_book.book_name = row[1]
            a_book.author = row[2]
            a_book.genre = row[3]
            a_book.late_fee = row[4]
            a_book.borrow_date = row[5]
            a_book.lost = row[6]
            a_book.borrower_id = row[7]

        if a_book.borrower_id != 0:
            print()
            print('Sorry the book is occupied')
        else:
            cursor_book.execute(update_book_query, l_borrower_id, today, book_id)
            cursor_book.commit()
            cursor_book.execute(get_book_info_query, book_id)
            for row in cursor_book:
                a_book.book_id = row[0]
                a_book.book_name = row[1]
                a_book.author = row[2]
                a_book.genre = row[3]
                a_book.late_fee = row[4]
                a_book.borrow_date = row[5]
                a_book.lost = row[6]
                a_book.borrower_id = row[7]

            return_date = a_book.borrow_date + datetime.timedelta(days=30)
            print('You should return before : {}, or you will be charged: {}$'.format(return_date, a_book.late_fee))

    def return_books(self):
        print()
        return_book_id = input('Enter ID\'s returning book: ')
        reset_borrower_id_query = '''UPDATE Books
                                    SET BorrowerID = 0, BorrowDate = ?
                                    WHERE BookID = ?'''
        cursor_book = conn.cursor()
        cursor_book.execute(reset_borrower_id_query, datetime.date.today(), return_book_id)
        cursor_book.commit()
        cursor_book.close()

    def get_book_id(self, l_borrower_id, l_book_id):
        cursor_book = conn.cursor()
        get_book_id_query = '''SELECT BookID 
                                FROM Books
                                WHERE Books.BorrowerID = ? AND Books.BookID = ?;'''
        cursor_book.execute(get_book_id_query, l_borrower_id, l_book_id)
        idd = -1
        for row in cursor_book:
            idd = int(row[0])

        return idd

    def report_lost_books(self, l_borrower_id):
        cursor_book = conn.cursor()

        l_book_id = int(input('Enter ID\'s lost book: '))
        l_book = Books()
        iddd = self.get_book_id(l_borrower_id, l_book_id)

        if iddd == l_book_id:
            # get lost fee, lost fee is Late fee * 3
            get_lost_fee_query = ''' SELECT LateFee*3, BookName
                                     FROM Books
                                     WHERE BookID = ?'''
            cursor_book.execute(get_lost_fee_query, iddd)
            lost_fee = 0
            book_name = ''
            for row in cursor_book:
                lost_fee = float(row[0])
                book_name = row[1]
            print('You pay {}$ for losing {}'.format(lost_fee, book_name))

            # get the current borrower's payment
            get_payment_query = '''SELECT Payment
                                    FROM Borrowers
                                    WHERE BorrowerID = ?'''
            cursor_book.execute(get_payment_query, l_borrower_id)
            new_payment = 0
            for row in cursor_book:
                new_payment = float(row[0])
            new_payment += lost_fee

            # Update the new payment(new payment = lost fee + latest payment)
            update_payment_query = '''UPDATE Borrowers
                                                  SET Payment = ?
                                                  WHERE BorrowerID = ?'''
            cursor_book.execute(update_payment_query, new_payment, l_borrower_id)
            cursor_book.commit()

            update_lost_query = '''UPDATE Books
                                    SET Lost = 1, BorrowerID = -1
                                    WHERE BorrowerID = ? and BookID = ?;'''
            cursor_book.execute(update_lost_query, l_borrower_id, iddd)
            cursor_book.commit()

            print()
            print()
            print('You report lost successfully')
        else:
            print()
            print('You do not have this book')

        cursor_book.close()


class Books:
    def __init__(self):
        self.book_id = -1
        self.book_name = ''
        self.author = ''
        self.genre = ''
        self.late_fee = 0
        self.borrow_date = datetime.date.today()
        self.lost = 0
        self.borrower_id = 0


def menu():
    x = -1
    while x != 0:
        try:
            print('Enter 1 to login')
            print('Enter 2 to register')
            print('Enter 0 to exit 205 Library')
            x = int(input('Input: '))
            if x < 0 or x > 2:
                raise ValueError('Invalid input')
            else:
                break

        except ValueError as excerpt:
            print(Fore.RED)
            print(excerpt)
            print(Fore.WHITE)
            print('Please enter from 0 to 2 to use the program')
            print()
    return x


def librarian_menu():
    x = -1
    while x != 0:
        try:
            print('Press 1 to create new book')
            print('Press 2 to create new librarian')
            print('Press 3 to delete a books')
            print('Press 4 to see all lost books')
            print('Press 5 to process user payment')
            print('Press 0 to return main menu')
            x = int(input('Enter a number: '))
            if x < 0 or x > 5:
                raise ValueError('Invalid input')
            else:
                break

        except ValueError as excerpt:
            print(Fore.RED)
            print(excerpt)
            print(Fore.WHITE)
            print('Please enter from 0 to 5 to use the program')
            print()
    return x


def borrower_menu():
    x = -1
    while x != 0:
        try:
            print('Press 1 to borrow new book')
            print('Press 2 to return a book')
            print('Press 3 to report lost')
            print('Press 0 to return main menu')
            x = int(input('Enter a number here: '))
            if x < 0 or x > 3:
                raise ValueError('Invalid input')
            else:
                break

        except ValueError as excerpt:
            print(Fore.RED)
            print(excerpt)
            print(Fore.WHITE)
            print('Please enter from 0 to 3 to use the program')
            print()
    return x

# ====================================================
# ======================= MAIN =======================
# ====================================================


user_input = menu()
while user_input != 0:
    if user_input == 1:
        email = input('Enter your email to login: ')
        password = getpass.getpass('Enter password: ')
#        email = 'rrey@my.bcit.ca'
#        password = 'Pa$$w0rd'
#        email = 'dvo12@my.bcit.ca'
#        password = 'Pa$$w0rd'
        login_borrower = get_borrower(email, password)
        login_librarian = get_librarian(email, password)
        os.system('cls')
        title_format = '{title:^172}'
        # if login user as borrower
        if login_borrower.id > 0:
            title_format = '{title:^172}'
            login_borrower.welcome_screen(login_borrower.last_name, login_borrower.first_name, 'Welcome to 205 Library')
            print(title_format.format(title='List of books are available'.upper()))
            login_borrower.list_books()
            login_borrower.print_empty_line(1)
            print(title_format.format(title='You are keeping these books'.upper()))
            login_borrower.list_books(login_borrower.id)
            login_borrower.print_empty_line(1)
            print(title_format.format(title='These books are being late return'.upper()))
            login_borrower.get_late_books(login_borrower.id)
            login_borrower.print_empty_line(1)
            now = str(datetime.date.today())
            payment = str(login_borrower.payment)
            print(title_format.format(
                title='Your total payment until ' + Fore.BLUE + now + Fore.WHITE + ' is ' + Fore.RED + payment + '$'))
            print(Fore.WHITE)
            login_borrower.print_empty_line(3)
            borrower_control = borrower_control = borrower_menu()
            while borrower_control != 0:
                if borrower_control == 1:
                    login_borrower.print_empty_line(1)
                    login_borrower.borrow_books(login_borrower.id)
                    login_borrower.print_empty_line(1)
                    borrower_control = borrower_menu()
                # return a book
                elif borrower_control == 2:
                    login_borrower.print_empty_line(1)
                    login_borrower.return_books()
                    login_borrower.print_empty_line(1)
                    borrower_control = borrower_menu()
                    # report lost
                elif borrower_control == 3:
                    login_borrower.print_empty_line(1)
                    login_borrower.report_lost_books(login_borrower.id)
                    login_borrower.print_empty_line(1)
                    borrower_control = borrower_menu()
        # Login user as an librarian account
        elif login_librarian.id > -1:
            login_librarian.welcome_screen(login_librarian.first_name, login_librarian.last_name, 'Have a good day!')
            print(Fore.WHITE + title_format.format(title='Available books in library:'.upper()))
            login_librarian.list_books()
            login_librarian.print_empty_line(3)
            librarian_control = librarian_menu()
            while librarian_control != 0:
                # create new books(Done!!!!)
                if librarian_control == 1:
                    login_librarian.print_empty_line(1)
                    login_librarian.create_book()
                    login_librarian.print_empty_line(1)
                    librarian_control = librarian_menu()
                # create new librarian(DONE!!!)
                elif librarian_control == 2:
                    login_librarian.print_empty_line(1)
                    login_librarian.create_librarians()
                    login_librarian.print_empty_line(1)
                    print('Librarian account created successfully!')
                    login_librarian.print_empty_line(1)
                    librarian_control = librarian_menu()
                # delete a book(DONE!!!!!)
                elif librarian_control == 3:
                    login_librarian.print_empty_line(1)
                    login_librarian.delete_books()
                    login_borrower.print_empty_line(1)
                    key = input('Press any key to continue')
                    librarian_control = librarian_menu()
                    login_borrower.print_empty_line(1)
                # listing all the lost books
                elif librarian_control == 4:
                    login_librarian.get_lost_books()
                    login_librarian.print_empty_line(1)
                    librarian_control = librarian_menu()
                    login_librarian.print_empty_line(1)
                # process user payment(DONE!!!!)
                elif librarian_control == 5:
                    login_librarian.print_empty_line(1)
                    login_librarian.payment()
                    login_librarian.print_empty_line(1)
                    librarian_control = librarian_menu()
        else:
            print('You typed wrong password or your account does not exist')
            login_borrower.print_empty_line(1)
            x = getpass.getpass('Press any key to return the main menu ')
        os.system('cls')
        user_input = menu()

    elif user_input == 2:
        create_user_account()
        user_input = menu()

    elif user_input == 0:
        print('See you again!')

conn.close()
