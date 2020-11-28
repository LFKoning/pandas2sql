"""Module for SQL generator classes."""

from pandas._libs.lib import infer_dtype


class SQLGenerator:
    """Base class for SQL generating classes."""

    # Map pandas to SQL data types
    _SQL_TYPES = {}

    def __init__(self, indent=2):
        self._indent = int(indent)

    def generate_schema(self, df, table_name, constraints=None):
        """
        Generates a CREATE TABLE statement from a pandas DataFrame.

        Parameters
        ----------
        df : pandas.DataFrame
            Pandas DataFrame to create a schema for.
        table_name : str
            Name for the target SQL table.
        constraints : list
            List of constraint objects to include in the schema.

        Returns
        -------
        str
            Create table SQL statement.
        """

        table_name = self._id(table_name)

        # Create column specifications from dtypes
        table_spec = [col + " " + dtype for col, dtype in self._map_dtypes(df).items()]

        # Create constraints (if provided)
        if constraints:
            for constraint in constraints:
                table_spec.append(constraint.make(self._id))

        table_spec = [" " * self._indent + line for line in table_spec]
        table_spec = ",\n".join(table_spec)

        return f"CREATE TABLE {table_name} (\n{table_spec}\n);\n"

    def generate_inserts(self, df, table_name):
        """
        Generates INSERT statements from a DataFrame.

        TO DO:
        - Double up single quotes
        """

        sql_texts = []
        for _, row in df.iterrows():
            sql_texts.append(
                f"INSERT INTO {table_name} ({', '.join(df.columns)}) "
                f"VALUES {str(tuple(row))}"
            )
        return sql_texts

    @staticmethod
    def _quote(value):
        """
        Quotes a (string) value for use in SQL statements.

        Parameters
        ----------
        value : str
            Value to put in quotes

        Returns
        -------
        str
            Quoted string.
        """

        return f"'{value}'"

    @staticmethod
    def _id(identifier):
        """
        Creates an identifier string for use in SQL statements.

        Parameters
        ----------
        identifier : str
            String to turn into an identifier.

        Returns
        -------
        str
            Identifier as string.
        """

        return f'"{identifier}"'

    def _lookup_dtype(self, dtype, col):
        """Look up a single dtype in _SQL_TYPES."""

        if dtype not in self._SQL_TYPES:
            raise TypeError(f"Unsupported data type '{dtype}' for column '{col}'.")
        return self._SQL_TYPES[dtype]

    def _map_dtypes(self, df):
        """Maps columns to SQL types."""

        return {
            self._id(col): self._lookup_dtype(infer_dtype(df[col]), col)
            for col in df.columns
        }


class MSSQLGenerator(SQLGenerator):
    """Class for generating MS SQL Server compatible SQL."""

    _SQL_TYPES = {
        "string": "TEXT",
        "floating": "REAL",
        "integer": "INTEGER",
        "datetime": "TIMESTAMP",
        "date": "DATE",
        "time": "TIME",
        "boolean": "INTEGER",
    }

    @staticmethod
    def _id(identifier):
        return f"[{identifier}]"


class MySQLGenerator(SQLGenerator):
    """Class for generating MySQL compatible SQL."""

    _SQL_TYPES = {
        "string": "TEXT",
        "floating": "REAL",
        "integer": "INTEGER",
        "datetime": "TIMESTAMP",
        "date": "DATE",
        "time": "TIME",
        "boolean": "INTEGER",
    }

    @staticmethod
    def _id(identifier):
        return f"`{identifier}`"


class PostgreSQLGenerator(SQLGenerator):
    """Class for generating PostgreSQL compatible SQL."""

    _SQL_TYPES = {
        "string": "TEXT",
        "floating": "REAL",
        "integer": "INTEGER",
        "datetime": "TIMESTAMP",
        "date": "DATE",
        "time": "TIME",
        "boolean": "INTEGER",
    }

    @staticmethod
    def _id(identifier):
        return f'"{identifier}"'


class SQLiteGenerator(SQLGenerator):
    """Class for generating SQLite compatible SQL."""

    _SQL_TYPES = {
        "string": "TEXT",
        "floating": "REAL",
        "integer": "INTEGER",
        "datetime": "TIMESTAMP",
        "date": "DATE",
        "time": "TIME",
        "boolean": "INTEGER",
    }

    @staticmethod
    def _id(identifier):
        return f'"{identifier}"'
