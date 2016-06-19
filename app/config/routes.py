from system.core.router import routes

routes['default_controller'] = 'Login'
routes['/login'] = 'Login#get_login'
routes['/register'] = 'Login#get_register'
routes['/logout'] = 'Login#logout'
routes['POST']['/login'] = 'Login#login'
routes['POST']['/register'] = 'Login#register'
routes['/books'] = 'Books#home'
routes['/books/add'] = 'Books#add'
routes['/books/<id>'] = 'Books#review'
routes['/users/<id>'] = 'Books#userprofile'
routes['/reviews/remove/<id>'] = 'Books#removereview'
routes['POST']['/books/add'] = 'Books#insertbook'
routes['POST']['/reviews/add/<id>'] = 'Books#addreview'