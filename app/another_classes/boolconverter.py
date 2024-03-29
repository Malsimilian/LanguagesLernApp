from werkzeug.routing import BaseConverter


class BoolConverter(BaseConverter):
    def to_python(self, value):
        return value.lower() in ['True', 'true', 'yes', '1']

    def to_url(self, value):
        return str(value).lower()
