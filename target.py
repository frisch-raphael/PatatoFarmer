import sqlite3
from typing import Optional
from urllib.parse import urlparse


class Target:
    def __init__(self,
                 url,
                 mode,
                 pass_user_lists: list[str] = [""],
                 additional_keywords: list[str] = [""],
                 status="todo",
                 login_param=None,
                 password_param=None,
                 id=None):
        self.id = id
        self.url = url
        self.mode = mode
        self.pass_user_lists = pass_user_lists
        self.additional_keywords = additional_keywords
        self.status = status
        self.login_param = login_param
        self.password_param = password_param

    @property
    def port(self):
        return urlparse(self.url).port

    def save_to_db(self):
        query = '''INSERT INTO targets (url, mode, pass_user_lists, additional_keywords, status, login_param, password_param)
                VALUES (:url, :mode, :pass_user_lists, :additional_keywords, :status, :login_param, :password_param)'''
        args = {
            'url': self.url,
            'mode': self.mode,
            'pass_user_lists': ','.join(self.pass_user_lists),
            'additional_keywords': ','.join(self.additional_keywords),
            'status': self.status,
            'login_param': self.login_param,
            'password_param': self.password_param,
        }
        Target._execute_query(query, args)

    def to_list(self):
        return [
            self.id,
            self.url,
            self.mode,
            self.pass_user_lists,
            self.additional_keywords,
            self.status,
            self.login_param,
            self.password_param,
        ]

    @staticmethod
    def _execute_query(query, args=None):
        conn = sqlite3.connect('targets.db')
        c = conn.cursor()
        if args:
            c.execute(query, args)
        else:
            c.execute(query)
        conn.commit()
        conn.close()

    @staticmethod
    def __fetch_targets(query, args=None) -> list['Target']:
        conn = sqlite3.connect('targets.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(query, args) if args else c.execute(query)
        targets = []
        for row in c.fetchall():
            target = Target(id=row['id'],
                            url=row['url'],
                            mode=row['mode'],
                            pass_user_lists=row['pass_user_lists'].split(','),
                            additional_keywords=row['additional_keywords'].split(
                                ','),
                            status=row['status'],
                            login_param=row['login_param'],
                            password_param=row['password_param'])
            targets.append(target)
        conn.close()
        return targets

    @staticmethod
    def list_all():
        query = 'SELECT * FROM targets'
        targets = Target.__fetch_targets(query)
        return targets

    @staticmethod
    def list_forms():
        query = 'SELECT * FROM targets WHERE mode LIKE "%form%"'
        targets = Target.__fetch_targets(query)
        return targets

    @staticmethod
    def list_standards():
        query = 'SELECT * FROM targets where mode NOT LIKE "%form%"'
        targets = Target.__fetch_targets(query)
        return targets

    @staticmethod
    def delete_by_id(id):
        query = 'DELETE FROM targets WHERE id = ?'
        args = (id,)
        Target._execute_query(query, args)

    @staticmethod
    def bulk_delete(start_id, end_id):
        query = 'DELETE FROM targets WHERE id BETWEEN ? AND ?'
        args = (start_id, end_id)
        Target._execute_query(query, args)

    @staticmethod
    def edit_by_id(id, new_target):
        query = 'UPDATE targets SET url=?, mode=?, pass_user_lists=?, additional_keywords=?, status=?, login_param=?, password_param=? WHERE id=?'
        args = (new_target.url, new_target.mode, ','.join(new_target.pass_user_lists), ','.join(
            new_target.additional_keywords), new_target.status, new_target.login_param, new_target.password_param, id)
        Target._execute_query(query, args)

    @staticmethod
    def bulk_edit(start_id, end_id, new_target):
        query = 'UPDATE targets SET url=?, mode=?, pass_user_lists=?, additional_keywords=?, status=?, login_param=?, password_param=?, WHERE id BETWEEN ? AND ?'
        args = (new_target.url, new_target.mode, ','.join(new_target.pass_user_lists), ','.join(
            new_target.additional_keywords), new_target.status, new_target.login_param, new_target.password_param, start_id, end_id)
        Target._execute_query(query, args)

    @staticmethod
    def find_by_id(id) -> Optional['Target']:
        query = 'SELECT * FROM targets WHERE id = ?'
        args = (id,)
        targets = Target.__fetch_targets(query, args)
        if targets:
            target = targets[0]
        else:
            target = None
        return target
