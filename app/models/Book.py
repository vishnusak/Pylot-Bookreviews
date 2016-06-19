from system.core.model import Model

class Book(Model):
    def __init__(self):
        super(Book, self).__init__()
        self.__query = ''
        self.__data = {}

    def run_query(self, query, data={}):
        return self.db.query_db(query, data)

    def check_for_books(self):
        self.__query = "SELECT count(*) as rows FROM books"
        self.__data = {}
        return self.run_query(self.__query, self.__data)[0]

    def get_authors(self):
        self.__query = "SELECT distinct(author) FROM books"
        self.__data = {}
        return self.run_query(self.__query, self.__data)

    def get_book_by_title(self, title):
        self.__query = "SELECT id, title, author FROM books WHERE title = :title"
        self.__data = {
            'title': title
        }
        return self.run_query(self.__query, self.__data)

    def get_book(self, id):
        self.__query = "SELECT id, title, author FROM books WHERE id = :id"
        self.__data = {
            'id': id
        }
        return self.run_query(self.__query, self.__data)[0]

    def get_reviewed_books(self):
        self.__query = "SELECT id, title, author FROM books"
        self.__data = {}
        return self.run_query(self.__query, self.__data)

    def get_recent_reviews(self):
        self.__query = "SELECT r.id as review_id, r.book_id as book_id, r.rating as book_rating, r.review_text as review, DATE_FORMAT(r.created_at,'%M %D, %Y') as date, b.title as book_name, u.alias as user_alias, r.user_id as user_id FROM reviews r, books b, users u WHERE r.user_id = u.id AND r.book_id = b.id ORDER BY r.created_at DESC LIMIT 3"
        self.__data = {}
        return self.run_query(self.__query, self.__data)

    def get_book_reviews(self, id):
        self.__query = "SELECT r.id as review_id, r.rating as book_rating, r.review_text as review, DATE_FORMAT(r.created_at,'%M %D, %Y') as date, u.alias as user_alias, r.user_id as user_id FROM reviews r, users u WHERE r.book_id = :id AND r.user_id = u.id ORDER BY r.created_at DESC"
        self.__data = {
            'id': id
        }
        return self.run_query(self.__query, self.__data)

    def insert_book(self, title, author):
        self.__query = "INSERT INTO books (title, author, created_at, modified_at) VALUES (:title, :author, NOW(), NOW())"
        self.__data = {
            'title': title,
            'author': author
        }
        return self.run_query(self.__query, self.__data)

    def insert_review(self, form, book_id, user_id):
        self.__query = "INSERT INTO reviews (book_id, user_id, review_text, rating, created_at, modified_at) VALUES (:book_id, :user_id, :review_text, :rating, NOW(), NOW())"
        self.__data = {
            'book_id': book_id,
            'user_id': user_id,
            'review_text': form['review'],
            'rating': form['rating']
        }
        return self.run_query(self.__query, self.__data)

    def delete_review(self, id):
        self.__query = "DELETE FROM reviews WHERE id = :id"
        self.__data = {
            'id': id
        }
        return self.run_query(self.__query, self.__data)

    def get_user_id(self, id):
        self.__query = "SELECT id, name, alias, email, password FROM users WHERE id = :id"
        self.__data = {
            'id': id
        }
        return self.run_query(self.__query, self.__data)[0]

    def get_user_review_count(self, id):
        self.__query = "SELECT count(*) AS reviews FROM reviews WHERE user_id = :id"
        self.__data = {
            'id': id
        }
        return self.run_query(self.__query, self.__data)[0]

    def get_user_reviewed_books(self, id):
        self.__query = "SELECT DISTINCT(concat(b.id, '|', b.title)) as book_dtl FROM reviews r, books b WHERE r.user_id = :id and r.book_id = b.id"
        self.__data = {
            'id': id
        }
        return self.run_query(self.__query, self.__data)
