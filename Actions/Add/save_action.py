from Actions.Add.back_action import BackAction
from Actions.base_action import BaseActionWithTarget
from logger import Logger


class SaveAction(BaseActionWithTarget):
    usage = """    save"""

    def execute(self, args):
        try:
            self.target.save_to_db()
            Logger.success("Saved target to db")
            BackAction(self.menu).execute()
        except Exception as e:
            Logger.warn(str(e))
