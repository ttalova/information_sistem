#!/usr/bin/env python

import cgi
import html
from util import Util
form = cgi.FieldStorage()
action = form.getfirst("action")

login = form.getfirst("login")
password = form.getfirst("password")

post = form.getfirst("text", "")
text = html.escape(post)
util = Util()

online = util.get_data(util.ONLINE)
user = online[0] if len(online) else None

error = False
message = ''

if action == "login":
    if util.login(login, password):
        user = login
    else:
        error = True
        message = '<p>Такой пользователь не зарегистрирован</p>'
elif action == "register":
    if not util.find(login):
        util.register(login, password)
        message = '<p>Вы зарегистрированы и уже авторизованы</p>'
    else:
        action = "logout"
        message = '<p>Вы уже зарегистрированы</p>'

elif action == 'posting':
    util.do_post(user, post)
elif action == "logout":
    util.logout(user)
    message = "<p>Вы вышли из системы</p>"
elif not action:
    if not util.is_online(user):
        action = "logout"

if action == "logout" or error:
    form = '''
        <form method="post" name='main_screen' action="wall.py">
        <h1>Войти:</h1>
            Логин: <input type="text" name="login">
            Пароль: <input type="password" name="password">
            <input type="hidden" name="action" value="login">
            <input type="submit">
        </form>
        <br>
        <form method="post" name='main_screen' action="wall.py">
        <h1>Регистрация</h1>
            Логин: <input type="text" name="login">
            Пароль: <input type="password" name="password">
            <input type="hidden" name="action" value="register">
            <input type="submit">
        </form>
    '''
else:
    form = '''
        <form name='my_site' action="wall.py">
            <p><b>Расскажите что-нибудь:</b></p>
            <p><textarea rows="10" cols="180" name="text"></textarea></p>
            <input type="hidden" name="action" value="posting">
            <input type="submit" value="Опубликовать">
        </form>
        <form name='my_site' action="wall.py">
            <input type="hidden" name="action" value="logout">
            <input type="submit" value="Выйти">
        </form>
    '''
pattern = '''
<!DOCTYPE HTML>
<html>
<head>
<meta charset="utf-8">
<title>Wall</title>
<link type="text/css" rel="stylesheet" href="/css/style.css"/>
</head>
<body>
    <div class='mess'>
    {message}
    </div>
    <div class='post'>
    {posts}
    </div>
    {form}
</body>
</html>
'''

print('Content-type: text/html\n')
print(pattern.format(form=form, posts = util.list_of_posts(user), message=message))