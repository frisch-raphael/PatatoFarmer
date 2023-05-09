from src.actions.add_targets.back_action import BackAction
from src.actions.base_action import BaseActionWithTarget
from src.utils.logger import Logger
from pony.orm import db_session
from src.enums.acg_count_options import ArgCountOptions
from src.models.target import Target


class SaveAction(BaseActionWithTarget):
    usage = """save"""
    arg_count_options = [ArgCountOptions.NONE]

    @db_session
    def _execute(self, args):
        try:
            Target.from_dto(self.target_dto)
            Logger.success("Saved target to db")
            BackAction(self.menu).execute()
        except Exception as e:
            Logger.warn(str(e))
