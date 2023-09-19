import abc


class Constraint:

    @abc.abstractmethod
    def validate(self, value):
        pass


class PrimaryKey(Constraint):
    name = 'primary_key'
    is_dml = False
    is_ddl = True

    def validate(self, value):
        pass


class NotNullConstraint(Constraint):
    name = 'not_null'
    is_dml = True
    is_ddl = False

    def validate(self, value):
        pass

    @staticmethod
    def validate_data(value):
        if value is None:
            raise ValueError('Null value not allowed.')
