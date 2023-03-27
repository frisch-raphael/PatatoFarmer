import pathlib
import readline


class ReadlineCompleter:
    def __init__(self, menu):
        self.menu = menu

    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        if buffer.lower().startswith("import_nmap"):
            incomplete_path = pathlib.Path(text)
            if incomplete_path.is_dir():
                completions = [p.as_posix() for p in incomplete_path.iterdir()]
            elif incomplete_path.exists():
                completions = [incomplete_path]
            else:
                exists_parts = pathlib.Path('.')
                for part in incomplete_path.parts:
                    test_next_part = exists_parts / part
                    if test_next_part.exists():
                        exists_parts = test_next_part

                completions = []
                for p in exists_parts.iterdir():
                    p_str = p.as_posix()
                    if p_str.startswith(text):
                        completions.append(p_str)
            return completions[state]
        else:
            ids = self.menu.get_ids()
            matches = [id for id in ids if id.startswith(text.lower())]
            try:
                return matches[state]
            except IndexError:
                return IndexError
