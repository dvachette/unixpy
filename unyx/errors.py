from __future__ import annotations

class Error:
    """
        -1 : File not found
        -2 : Invalid parameter
        -3 : Missing parameter
        -4 : Internal error
        -5 : Access error
        -6 : Generic error
    """
    codes = {
        -1:"File not found",
        -2:"Invalid parameter",
        -3:"Missing parameter",
        -4:"Internal error",
        -5:"Access error",
        -6:"Generic error"
    }
    def __init__(self, code:int):
        self._code = code
        self._details:list[str] = list()
    def add_description(self, text:str|list[str]):
        if isinstance(text, str):
            text = [text]
        self._details.extend(text)
    
    def __repr__(self):
        text_ = f'Error {self._code}: {self.codes[self._code]}\n'
        text_ += '\n'.join(self._details)
        return text_
    
    def __str__(self):
        return repr(self)
