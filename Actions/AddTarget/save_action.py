from Actions.AddTarget.back_action import BackAction
from Actions.base_action import BaseActionWithTarget
from Classes.logger import Logger
from pony.orm import db_session
from Model.target import Target


class SaveAction(BaseActionWithTarget):
    usage = """    save"""

    @db_session
    def execute(self, args):
        try:
            Target.from_dto(self.target_dto)
            Logger.success("Saved target to db")
            BackAction(self.menu).execute()
        except Exception as e:
            Logger.warn(str(e))
