import sqlite3


class Target:
    def __init__(self, hostname, mode, port, wordlists="", additional_keywords="", status="todo", login_param=None, password_param=None, id=None, path=None):
        self.id = id
        self.hostname = hostname
        self.mode = mode
        self.port = port
        self.wordlists = wordlists
        self.additional_keywords = additional_keywords
        self.status = status
        self.login_param = login_param
        self.password_param = password_param
        self.path = path

    def save_to_db(self):
        query = 'INSERT INTO targets (hostname, mode, port, wordlists, additional_keywords, status, login_param, password_param, path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        args = (self.hostname, self.mode, self.port, '|'.join(self.wordlists), '|'.join(
            self.additional_keywords), self.status, self.login_param, self.password_param, self.path)
        Target._execute_query(query, args)

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
    def _fetch_targets(query, args=None):
        conn = sqlite3.connect('targets.db')
        c = conn.cursor()
        c.execute(query, args) if args else c.execute(query)
        targets = []
        for row in c.fetchall():
            target = Target(id=row[0],
                            hostname=row[1],
                            mode=row[2],
                            port=row[3],
                            wordlists=row[4].split('|'),
                            additional_keywords=row[5].split('|'),
                            status=row[6],
                            login_param=row[7],
                            password_param=row[8],
                            path=row[9])
            targets.append(target)
        conn.close()
        return targets

    @staticmethod
    def list_all():
        query = 'SELECT * FROM targets'
        targets = Target._fetch_targets(query)
        return targets

    @staticmethod
    def list_forms():
        query = 'SELECT * FROM targets WHERE mode LIKE "%form%"'
        targets = Target._fetch_targets(query)
        return targets

    @staticmethod
    def list_standards():
        query = 'SELECT * FROM targets where mode NOT LIKE "%form%"'
        targets = Target._fetch_targets(query)
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
        query = 'UPDATE targets SET hostname=?, mode=?, port=?, wordlists=?, additional_keywords=?, status=?, login_param=?, password_param=?, path=? WHERE id=?'
        args = (new_target.hostname, new_target.mode, new_target.port, '|'.join(new_target.wordlists), '|'.join(
            new_target.additional_keywords), new_target.status, new_target.login_param, new_target.password_param, new_target.path, id)
        Target._execute_query(query, args)

    @staticmethod
    def edit_by_id(id, new_target):
        query = 'UPDATE targets SET hostname=?, mode=?, port=?, wordlists=?, additional_keywords=?, status=?, login_param=?, password_param=?, path=? WHERE id=?'
        args = (new_target.hostname, new_target.mode, new_target.port, '|'.join(new_target.wordlists), '|'.join(
            new_target.additional_keywords), new_target.status, new_target.login_param, new_target.password_param, new_target.path, id)
        Target._execute_query(query, args)

    @staticmethod
    def bulk_edit(start_id, end_id, new_target):
        query = 'UPDATE targets SET hostname=?, mode=?, port=?, wordlists=?, additional_keywords=?, status=?, login_param=?, password_param=?, path=? WHERE id BETWEEN ? AND ?'
        args = (new_target.hostname, new_target.mode, new_target.port, '|'.join(new_target.wordlists), '|'.join(
            new_target.additional_keywords), new_target.status, new_target.login_param, new_target.password_param, new_target.path, start_id, end_id)
        Target._execute_query(query, args)

    @staticmethod
    def find_by_id(id):
        query = 'SELECT * FROM targets WHERE id = ?'
        args = (id,)
        targets = Target._fetch_targets(query, args)
        if targets:
            target = targets[0]
        else:
            target = None
        return target
