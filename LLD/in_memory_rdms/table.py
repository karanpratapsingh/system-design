import constraints, fields


class Column:

    def __init__(self, name, field_type: fields.Field, column_constraints):
        self.field_type = field_type
        self.name = name
        self.constraints = column_constraints
        self.validate()

    def validate(self):
        self.field_type.validate()
        for constraint in self.constraints:
            constraint.is_ddl and constraint.validate()

    def validate_value(self, value):
        self.field_type.validate_data(value)
        for constraint in self.constraints:
            constraint.is_dml and constraint.validate_data(value)


class Table:
    def __init__(self, name, columns):
        self.name = name
        self.column_map = {column.name: column for column in columns}
        self.rows = []

    def add_record(self, data_mapping):
        if list(data_mapping.keys()) != list(self.column_map.keys()):
            raise ValueError('columns mismatch')

        for name, value in data_mapping.items():
            self.column_map[name].validate_value(value)
        self.rows.append(data_mapping)

    @staticmethod
    def print_record(rows):
        if rows:
            for row in rows:
                for name, value in row.items():
                    print(f'{name}: {value}')
                print()
        else:
            print('no record found')

    def get_record(self, filters=None):
        if filters is None:
            filters = {}
        for name, value in filters.items():
            if name in self.column_map:
                self.column_map[name].validate_value(value)
            else:
                raise ValueError(f"Column '{name}' not found is table")
        filtered_record = []
        for row in self.rows:
            matched = True
            for name, value in filters.items():
                if row[name] is not value:
                    matched = False
                    break
            if matched:
                filtered_record.append(row)
        return filtered_record


def main():

    new_columns = [
        Column('id', fields.IntegerField(), [constraints.NotNullConstraint(), constraints.PrimaryKey()]),
        Column('name', fields.StringField(max_length=10), [constraints.NotNullConstraint()]),
        Column('age', fields.IntegerField(min_value=0, max_value=100), [constraints.NotNullConstraint()])
    ]
    new_table = Table('student', columns=new_columns)
    new_table.add_record({'id': 1, 'name': 'shivam', 'age': 10})
    new_table.add_record({'id': 2, 'name': 'shivam', 'age': 20})
    new_table.add_record({'id': 3, 'name': 'jindal', 'age': 2})
    new_table.print_record(new_table.get_record({'name': 'shivam', 'id': 2}))

main()
