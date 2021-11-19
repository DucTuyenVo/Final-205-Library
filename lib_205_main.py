import pyodbc
import datetime

# scan all the drivers
#for driver in pyodbc.drivers():
#    print(driver)

# define the connection
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=DESKTOP-MIEL300\SQLEXPRESS;'
                      'Database=Lib_205;'
                      'Trusted_Connection=yes;')


# Create connection
# cursor_users = conn.cursor()
# cursor_books = conn.cursor()

def create_user_account():
    cursor_users = conn.cursor()
    insert_user_query = '''INSERT INTO Lib_User(FirstName, LastName, LoginName, Password, Email, Payment, FavoriteGenre)
                           VALUES (?,?,?,?,?,?,?);'''
    # get user inputs
    user_first_name = input('Enter your first name: ')
    user_last_name = input('Enter your last name: ')
    user_login_name = user_last_name[0] + user_last_name
    user_password = input('Enter your password: ')
    user_email = input('Enter your email: ')
    user_payment = 0
    user_favorite_genre = input('Enter your favorite genre: ')

    # insert into table Lib_user
    cursor_users.execute(insert_user_query, user_first_name, user_last_name, user_login_name,
                         user_password, user_email, user_payment, user_favorite_genre)

    # confirm the insert
    cursor_users.commit()
    # close the connections
    cursor_users.close()
    conn.close()

    return 1


def create_book():
    cursor_books = conn.cursor()
    insert_book_query = '''INSERT INTO Books (BookName, Author, Genre, LateFee, BorrowDate, BorrowerID)
                            VALUES (?,?,?,?,?,?);'''
    #   book_id = input('Enter book ID: ')
    book_name = input('Enter book name: ')
    author_name = input('Enter author name: ')
    genre = input('Enter book genre: ')
    late_fee = input('Enter fee for late return: ')
    borrow_date = datetime.date.today()
    # New book ID will be 0 which is belong to SYSTEM USER
    borrower_id = 0
    cursor_books.execute(insert_book_query, book_name, author_name, genre, late_fee, borrow_date, borrower_id)
    cursor_books.commit()
    cursor_books.close()
    conn.close()
    return 1


# ====================================================
# ======================= MAIN =======================
# ====================================================

# create_user_account()
