import abc


class Field:
    DATA_TYPE = NotImplemented

    @abc.abstractmethod
    def validate(self, *args, **kwargs):
        pass

    def validate_data(self, value):
        if not isinstance(value, self.DATA_TYPE):
            raise TypeError


class StringField(Field):
    SUPPORTED_MAX_LENGTH = 20
    DATA_TYPE = str

    def __init__(self, max_length):
        self.max_length = max_length

    def validate(self):
        if self.max_length > self.SUPPORTED_MAX_LENGTH:
            raise ValueError(f'Supported max length is {self.SUPPORTED_MAX_LENGTH}')

    def validate_data(self, value):
        super(StringField, self).validate_data(value)
        if len(value) > self.max_length:
            raise ValueError('extra length')


class IntegerField(Field):
    SUPPORTED_MIN_VALUE = -1024
    SUPPORTED_MAX_VALUE = 1024
    DATA_TYPE = int

    def __init__(self, min_value=None, max_value=None):
        self.min_value = self.SUPPORTED_MIN_VALUE if min_value is None else min_value
        self.max_value = self.SUPPORTED_MAX_VALUE if max_value is None else max_value

    def validate(self):
        if self.min_value > self.max_value:
            raise ValueError('min_value should not be greater than max_value')
        if self.min_value < self.SUPPORTED_MIN_VALUE:
            raise ValueError('min_value error')
        if self.max_value > self.SUPPORTED_MAX_VALUE:
            raise ValueError('max_value error')

    def validate_data(self, value):
        super(IntegerField, self).validate_data(value)
        if value and value > self.max_value:
            raise ValueError('extra value')
        if value and value < self.min_value:
            raise ValueError('less value')
