from system.core.controller import *

class Login(Controller):
    def __init__(self, action):
        super(Login, self).__init__(action)
        self.load_model('Login')
        self.__db = self.models['Login']

    def __session_init(self):
        if 'user_id' not in session:
            session['user_id'] = ''
        if 'user_name' not in session:
            session['user_name'] = ''
        if 'user_alias' not in session:
            session['user_alias'] = ''
        if 'user_email' not in session:
            session['user_email'] = ''
        if 'profile' not in session:
            session['profile'] = {}
        if 'err' not in session:
            session['err'] = {}
        if 'form' not in session:
            session['form'] = {}
        if 'authors' not in session:
            session['authors'] = []
        if 'book' not in session:
            session['book'] = {}
        if 'recent_reviews' not in session:
            session['recent_reviews'] = []
        if 'reviewed_books' not in session:
            session['reviewed_books'] = []

    def index(self):
        session.clear()
        self.__session_init()
        return self.load_view('login.html')

    def home(self):
        if session['user_id']:
            books = self.__db.check_for_books()
            if books['rows'] > 0:
                return self.load_view('home.html')
            else:
                return redirect('/books/add')
        else:
            return redirect('/')

    def get_login(self):
        return redirect('/')

    def get_register(self):
        return redirect('/')

    def logout(self):
        return redirect('/')

    def login(self):
        user_email = request.form['email'] if request.form['email'] else ''
        user_pwd = request.form['pwd'] if request.form['pwd'] else ''
        #
        email_isValid = self.__db.lemail_validate(user_email)
        pwd_isValid = self.__db.lpwd_validate(user_pwd)
        user = self.__db.login(request.form)

        session['err'] = {}
        session['form'] = {}

        if not email_isValid['status']:
            session['err'].update(email_isValid['msg'])
        else:
            session['form']['lemail'] = user_email

        if not pwd_isValid['status']:
            session['err'].update(pwd_isValid['msg'])

        if not user['status']:
            session['err'].update(user['msg'])

        if not session['err']:
            session['form'] = {}
            session['user_id'] = user['msg']['id']
            session['user_name'] = user['msg']['name']
            session['user_alias'] = user['msg']['alias']
            session['user_email'] = user['msg']['email']
            return redirect('/books')
        else:
            return self.load_view('login.html')

    def register(self):
        user_name = request.form['name'] if request.form['name'] else ''
        user_alias = request.form['alias'] if request.form['alias'] else ''
        user_email = request.form['email'] if request.form['email'] else ''
        user_pwd = request.form['pwd'] if request.form['pwd'] else ''
        user_cpwd = request.form['cpwd'] if request.form['cpwd'] else ''

        name_isValid = self.__db.name_validate(user_name)
        alias_isValid = self.__db.alias_validate(user_alias)
        email_isValid = self.__db.remail_validate(user_email)
        pwd_isValid = self.__db.rpwd_validate(user_pwd, user_cpwd)

        session['err'] = {}
        session['form'] = {}

        if not name_isValid['status']:
            session['err'].update(name_isValid['msg'])
        else:
            session['form']['name'] = user_name

        if not alias_isValid['status']:
            session['err'].update(alias_isValid['msg'])
        else:
            session['form']['alias'] = user_alias

        if not email_isValid['status']:
            session['err'].update(email_isValid['msg'])
        else:
            session['form']['email'] = user_email

        if not pwd_isValid['status']:
            session['err'].update(pwd_isValid['msg'])

        if not session['err']:
            session['form'] = {}
            user = self.__db.register(request.form)
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_alias'] = user['alias']
            session['user_email'] = user['email']
            return redirect('/books')
        else:
            return self.load_view('login.html')
