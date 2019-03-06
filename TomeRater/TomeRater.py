class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print(self.name + "’s email has been updated!")

    def __repr__(self):
        return 'User: ' + self.name + ', Email: ' + self.email + ', books read: ' + str(len(self.books))

    def __eq__(self, other_user):
        if (self.name == other_user.name and
                self.email == other_user.email):
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        if len(list(filter(None, self.books.values()))) == 0:
            print('no read books')
            return 0
        return sum(filter(None, self.books.values())) / len(list(filter(None, self.books.values())))


class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print(self.title + "'s ISBN has been updated")

    def add_rating(self, rating):
        if rating < 0 or rating > 4:
            print("Invalid Rating")
        else:
            self.ratings.append(rating)

    def __eq__(self, other):
        if (self.title == other.title
                and self.isbn == other.isbn):
            return True
        else:
            return False

    # I added this in case we have book with no type and we want to print it.
    def __repr__(self):
        return self.title

    def get_average_rating(self):
        if len(list(filter(None, self.ratings))) == 0:
            print('no ratings')
            return 0
        return sum(filter(None, self.ratings)) / len(list(filter(None, self.ratings)))

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return self.title + ' by ' + self.author


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return self.title + ', a ' + self.level + ' manual on ' + self.subject


class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        if email not in self.users:
            print('No user with email '+email+'!')
        else:
            self.users[email].read_book(book, rating)
            if rating is not None:
                book.add_rating(rating)
            flag = False
            for b in self.books:
                if b == book:
                    self.books[book] += 1
                    flag = True
            if not flag:
                self.books[book] = 1

    def add_user(self, name, email, user_books=None):
        new_user = User(name, email)
        self.users[email] = new_user
        if user_books is not None:
            for b in user_books:
                self.add_book_to_user(b, email)

    def print_catalog(self):
        for b in self.books.keys():
            print(b)

    def print_users(self):
        for u in self.users.values():
            print(u)

    def most_read_book(self):
        max_read = 0
        for i in list(self.books.items()):
            if i[1] > max_read:
                max_read = i[1]
                max_book = i[0]
        return max_book

    def highest_rated_book(self):
        max_avg = 0
        for i in self.books.keys():
            b_avg = i.get_average_rating()
            if b_avg > max_avg:
                max_avg = b_avg
                max_book = i
        return max_book

    def most_positive_user(self):
        max_avg = 0
        for u in self.users.values():
            u_avg = u.get_average_rating()
            if u_avg > max_avg:
                max_avg = u_avg
                max_user = u
        return max_user

    def __repr__(self):
        return 'This Tome Rater includes ' + str(len(self.users)) +' users and ' + str(len(self.books))+ ' books.'

    # 2 tome raters are equal if they contain exactly the same books (doesn't depend on # of read or rating)
    # and same email users (doesn't depend on names).
    def __eq__(self, other):
        if (len(self.books) != len(other.books)) or (len(self.users) != len(other.users)):
            return False
        for key_b in self.books.keys():
            if key_b not in other.books.keys():
                return False
        for key_u in self.users.keys():
            if key_u not in other.users.keys():
                return False
        return True
