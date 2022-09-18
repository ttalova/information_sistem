#!/usr/bin/env python

import json
import os


class Util:
    USERS = "cgi-bin/users.json"
    ONLINE = "cgi-bin/online.json"
    POSTS = 'cgi-bin/posts.json'

    def __init__(self):
        def create_file(path, content):
            if not os.path.exists(path) or not os.stat(path).st_size:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(content, f)

        create_file(self.USERS, {})
        create_file(self.ONLINE, [])
        create_file(self.POSTS, {})

    def get_data(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data

    def set_data(self, path, content):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(content, f)

    def is_online(self, user):
        return user in self.get_data(self.ONLINE)

    def find(self, user):
        return user in self.get_data(self.USERS)

    def login(self, login, password):
        if self.find(login) and self.check_password(login, password):
            self.set_online(login)
            return True

        return False

    def register(self, login, password):
        if not self.find(login):
            users = self.get_data(self.USERS)
            users[login] = password
            self.set_data(self.USERS, users)
            self.set_online(login)

    def logout(self, user):
        online = self.get_data(self.ONLINE)
        if user in online:
            online.remove(user)
        self.set_data(self.ONLINE, online)

    def set_online(self, user):
        online = self.get_data(self.ONLINE)
        if user not in online:
            online += [user]
            self.set_data(self.ONLINE, online)

    def check_password(self, login, password):
        users = self.get_data(self.USERS)
        return users[login] == password

    def do_post(self, login, post):
        post_t = self.get_data(self.POSTS)
        post_t.setdefault(login, [])
        post_t[login].append(post)
        self.set_data(self.POSTS, post_t)

    def list_of_posts(self, user):
        """Список постов для отображения на странице"""
        if self.is_online(user):
            posts = self.get_data(self.POSTS)
            users_posts = []
            for post in posts[user]:
                content = user + ' : ' + post
                users_posts.append(content)
            return '<br>'.join(users_posts)
        else:
            return ''
