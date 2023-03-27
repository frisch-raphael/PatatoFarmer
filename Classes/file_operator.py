import os
from Classes.logger import Logger


class FileOperator:

    @staticmethod
    def delete(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            Logger.success(f"The file '{file_path}' has been deleted.")
        else:
            Logger.warn(f"The file '{file_path}' does not exist.")

    @staticmethod
    def read(file_path):
        if not os.path.exists(file_path):
            raise (FileNotFoundError(
                f"The file '{file_path}' does not exist."))
        with open(file_path, 'r') as file:
            content = file.read()
        return content
