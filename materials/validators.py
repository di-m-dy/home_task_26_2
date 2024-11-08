import re
from django.core.exceptions import ValidationError


class NoLinkValidator:
    """
    Пользовательский валидатор для проверки наличия ссылок в тексте
    """

    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, value):
        # Ensure value is a string, or retrieve the specific field if it's a dictionary
        if isinstance(value, dict):
            value = value.get(self.field_name, '')  # Fallback to an empty string if field is missing
        if not isinstance(value, str):
            raise ValidationError(f"{self.field_name} должен быть строкой.")

        # Check for links in the text
        if re.search(r'http://|https://', value):
            raise ValidationError('Ссылки в тексте не допустимы')
