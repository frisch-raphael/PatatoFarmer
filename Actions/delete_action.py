import re
from typing import List
from Actions.base_action import BaseAction
from logger import Logger
from target import Target


class DeleteAction(BaseAction):
    usage = """    Delete targets from the database
    
    delete USAGE:
    delete <target_id_1> [<target_id_2> ... <target_id_n>]
    delete <start_id-end_id>

    EXAMPLES:
    delete 1
    delete 1 3 4
    delete 10-20
    delete 1 4 5 10-20"""

    def execute(self, args: List[str]):
        # Define regular expression to match either an integer or a range of integers
        valid_arg_regex = r'^\d+$|^\d+-\d+$'

        # Check if any argument is invalid
        invalid_args = [
            arg for arg in args if not re.match(valid_arg_regex, arg)]
        if invalid_args or not args:
            print(self.usage)
            return

        # Split args by '-' to see if it's a range of ids
        ids = []
        for arg in args:
            if '-' in arg:
                # If it's a range, add all ids in the range
                start_id, end_id = arg.split('-')
                ids += list(range(int(start_id), int(end_id)+1))
            else:
                # If it's a single id, add it to the list
                ids.append(int(arg))

        # Delete targets for each id
        for id in ids:
            target = Target.find_by_id(id)
            if target:
                target.delete_by_id(id)
                Logger.success(f"Target with ID {id} deleted successfully")
            else:
                Logger.warn(
                    f"Target with ID {id} not found in database")
