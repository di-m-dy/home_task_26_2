import re

class NoLinkValidator:
    """
    Пользовательский валидатор для проверки наличия ссылок в тексте
    """
    def __init__(self, field_name):
        self.field_name = field_name
    def __call__(self, value):
        if re.search(r'http://|https://', value):
            raise ValueError('Ссылки в тексте не допустимы')
