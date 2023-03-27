from typing import Optional


class TargetDto:
    def __init__(self,
                 url: Optional[str] = None,
                 mode: Optional[str] = None,
                 status: str = "todo",
                 additional_keywords: Optional[list[str]] = None,
                 pass_user_lists: Optional[list[str]] = None,
                 login_param: Optional[str] = None,
                 password_param: Optional[str] = None):
        self.url = url
        self.mode = mode
        self.status = status
        self.additional_keywords = additional_keywords
        self.pass_user_lists = pass_user_lists
        self.login_param = login_param
        self.password_param = password_param
