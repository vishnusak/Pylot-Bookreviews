from system.core.controller import *

class Books(Controller):
    def __init__(self, action):
        super(Books, self).__init__(action)
        self.load_model('Book')
        self.__db = self.models['Book']

    def home(self):
        if session['user_id']:
            books = self.__db.check_for_books()
            if books['rows'] > 0:
                session['recent_reviews'] = self.__db.get_recent_reviews()
                session['reviewed_books'] = self.__db.get_reviewed_books()
                return self.load_view('home.html')
            else:
                return redirect('/books/add')
        else:
            return redirect('/')

    def add(self):
        authors = self.__db.get_authors()
        session['authors'] = authors
        return self.load_view('addbook.html')

    def insertbook(self):
        print request.form
        book_title = request.form['title'] if request.form['title'] else ''
        book_author = request.form['author_select'] if request.form['author_select'] else request.form['author'] if request.form['author'] else ''
        book_review = request.form['review'] if request.form['review'] else ''
        book_rating = request.form['rating'] if request.form['rating'] else ''

        session['err'] = {}
        session['form'] = {}

        if len(book_title) == 0:
            session['err']['title'] = '** Book must have title **'
        elif len(book_title) > 0:
            book_isPresent = self.__db.get_book_by_title(book_title)
            if book_isPresent:
                session['err']['title'] = '** Book already added **'
            else:
                session['form']['title'] = book_title
        else:
            session['form']['title'] = book_title

        if len(book_author) == 0:
            session['err']['author'] = '** Book must have author **'
        else:
            session['form']['author'] = book_author

        if len(book_review) == 0:
            session['err']['review'] = '** Book must have a review **'
        else:
            session['form']['review'] = book_review

        if len(book_rating) == 0:
            session['err']['rating'] = '** Book must have a rating **'

        if session['err']:
            return self.load_view('addbook.html')
        else:
            session['form'] = {}
            book_id = self.__db.insert_book(book_title, book_author)
            review_id = self.__db.insert_review(request.form, book_id, session['user_id'])
            return redirect('/books/'+str(book_id))

    def review(self, id):
        session['book'] = self.__db.get_book(id)
        session['book']['reviews'] = self.__db.get_book_reviews(id)
        return self.load_view('book.html')

    def removereview(self, id):
        self.__db.delete_review(id)
        return redirect('/books/'+str(session['book']['id']))

    def addreview(self, id):
        book_review = request.form['review'] if request.form['review'] else ''
        book_rating = request.form['rating'] if request.form['rating'] else ''

        session['err'] = {}
        session['form'] = {}

        if len(book_review) == 0:
            session['err']['review'] = '** Book must have a review **'
        else:
            session['form']['review'] = book_review

        if len(book_rating) == 0:
            session['err']['rating'] = '** Book must have a rating **'

        if session['err']:
            return redirect('/books/'+str(id))
        else:
            session['form'] = {}
            review_id = self.__db.insert_review(request.form, id, session['user_id'])
            return redirect('/books/'+str(id))

    def userprofile(self, id):
        session['profile'] = self.__db.get_user_id(id)
        session['profile'].update(self.__db.get_user_review_count(id))
        profile_books = self.__db.get_user_reviewed_books(id)
        session['profile']['books'] = [book['book_dtl'].partition('|') for book in profile_books]
        return self.load_view('user.html')
