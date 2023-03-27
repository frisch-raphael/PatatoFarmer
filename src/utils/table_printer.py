from prettytable import PrettyTable, DOUBLE_BORDER, ALL
from pony.orm import db_session
from src.dtos.target_dto import TargetDto
from src.models.wordlist import Wordlist


class TargetInfoMixin:

    @classmethod
    def create_target_dict(cls, target: TargetDto, fields):

        target_info = {
            'ID': getattr(target, 'id', None),
            'url': target.url,
            'Mode': target.mode,
            'Pass / User Lists': cls.__display_wordlists(target.pass_user_lists),
            'Additional Keywords': ", ".join(target.additional_keywords or []),
            'Login Param': getattr(target, 'login_param', None),
            'Password Param': getattr(target, 'password_param', None),
            'Status': target.status
        }
        return {k: target_info[k] for k in fields}

    @classmethod
    def __display_wordlists(cls, lists):
        if not lists:
            return ""
        if len(lists) > 1:
            return "\n".join([f"{i+1}- {t}" for i, t in enumerate(lists)])
        return lists[0]

    shared_fields = ["url", "Mode",
                     "Pass / User Lists", "Additional Keywords", "Status"]
    forms_fields = ["ID"] + shared_fields + ["Login Param", "Password Param"]
    standard_fields = ["ID"] + shared_fields


class TablePrinter(TargetInfoMixin):

    @staticmethod
    def prepare_table(field_names=None, title=None):
        table = PrettyTable()
        table.set_style(DOUBLE_BORDER)
        table.hrules = ALL
        if title:
            table.title = title
        if field_names:
            table.field_names = field_names
        return table

    @classmethod
    def show_target(cls, target):
        field_names = cls.shared_fields
        table = cls.prepare_table()
        target_dict = cls.create_target_dict(target, field_names)

        table.add_column("Attribute", field_names)
        table.add_column("Value", [target_dict[field_name]
                         for field_name in field_names])

        print()
        print(table)
        print()

    @classmethod
    def print_target_table(cls, targets, title, field_names):
        table = cls.prepare_table(field_names, title)

        for target in targets:
            target_dict = cls.create_target_dict(target, field_names)
            table.add_row([target_dict[field_name]
                          for field_name in table.field_names])

        print()
        print(table)
        print()

    @staticmethod
    @db_session
    def print_wordlist_table(wordlist_type, title):
        wordlists = Wordlist.select(lambda w: w.type == wordlist_type)[:]
        if not wordlists:
            return
        field_names = ["ID", "Name", "Path", "Type"]
        table = TablePrinter.prepare_table(field_names, title)

        for wordlist in wordlists:
            wordlist_dict = {
                'ID': wordlist.id,
                'Name': wordlist.name,
                'Path': wordlist.path,
                'Type': wordlist.type
            }
            table.add_row([wordlist_dict[field_name]
                          for field_name in table.field_names])

        print()
        print(table)
