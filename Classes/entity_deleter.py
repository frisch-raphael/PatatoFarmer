from typing import List
from pony.orm import db_session, ObjectNotFound
import re
from .logger import Logger


class EntityDeleter:
    @staticmethod
    def generate_delete_usage_string(entity_name: str) -> str:
        usage = f"""Delete {entity_name}s from the database

        {entity_name.lower()} delete USAGE:
        {entity_name.lower()} delete <{entity_name.lower()}_id_1> [<{entity_name.lower()}_id_2> ... <{entity_name.lower()}_id_n>]
        {entity_name.lower()} delete <start_id-end_id>

        EXAMPLES:
        {entity_name.lower()} delete 1
        {entity_name.lower()} delete 1 3 4
        {entity_name.lower()} delete 10-20
        {entity_name.lower()} delete 1 4 5 10-20"""

        return usage

    @staticmethod
    @db_session
    def delete_ids(entity_cls, args: List[str]):
        # Define regular expression to match either an integer or a range of integers
        valid_arg_regex = r'^\d+$|^\d+-\d+$'

        # Check if any argument is invalid
        invalid_args = [
            arg for arg in args if not re.match(valid_arg_regex, arg)]
        if invalid_args or not args:
            Logger.warn(
                'Invalid id format. Example of valid formats: "1", "1-10", "1 2 3 4 5-10"')
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

        # Delete entities for each id
        for id in ids:
            try:
                entity = entity_cls[id]
                entity.delete()
                Logger.success(
                    f"{entity_cls.__name__} with ID {id} deleted successfully")
            except ObjectNotFound:
                Logger.warn(
                    f"{entity_cls.__name__} with ID {id} not found in database")
