"""Module for SQL generator classes."""

from pandas._libs.lib import infer_dtype


class SQLGenerator:
    """Base class for SQL generating classes."""

    # Map pandas to SQL data types
    _SQL_TYPES = {
        "string": "TEXT",
        "floating": "REAL",
        "integer": "INTEGER",
        "datetime": "TIMESTAMP",
        "datetime64": "TIMESTAMP",
        "date": "DATE",
        "time": "TIME",
        "boolean": "INTEGER",
    }

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

    def generate_inserts(self, df, table_name, batch=100):
        """
        Generates INSERT statements from a DataFrame.

        Parameters
        ----------
        Parameters
        ----------
        df : pandas.DataFrame
            Pandas DataFrame to create a schema for.
        table_name : str
            Name for the target SQL table.
        batch : Optional[int]
            Batch size for the INSERT statement, defaults to 100.

        Returns
        -------
        str
            Insert statements for the provided DataFrame.
        """

        # Build statement parts and template
        table_name = self._id(table_name)
        column_spec = ", ".join([self._id(col) for col in df.columns])
        insert_tmpl = (
            "INSERT INTO {table_name} ({column_spec})\nVALUES\n{values}\n;\n\n"
        )
        row_tmpl = " " * self._indent + "({values})"

        # Convert the data to string format
        df = (
            df
            # Properly format the different data types
            .apply(self._convert_series, axis=0)
            # Concatenate the rows
            .apply(
                lambda row: row_tmpl.format(values=", ".join(row.astype(str))), axis=1
            )
            # Only keep the values
            .values
        )

        inserts = ""
        for idx in range(0, len(df), batch):
            values = df[idx : idx + batch]
            values = ",\n".join(values)

            inserts += insert_tmpl.format(
                table_name=table_name, column_spec=column_spec, values=values
            )

        return inserts

    @staticmethod
    def _id(identifier):
        """Creates an identifier string for use in SQL statements."""

        return f'"{identifier}"'

    @staticmethod
    def _quote(value):
        """Quotes a (string) value for use in SQL statements."""

        value = value.replace("'", "''")
        return f"'{value}'"

    def _date(self, value):
        """Formats a date value for use in SQL statements."""

        value = value.strftime(format="%Y%m%d")
        return self._quote(value)

    def _datetime(self, value):
        """Formats a datetime value for use in SQL statements."""

        value = value.strftime(format="%Y%m%dT%H:%M:%S%z")
        return self._quote(value)

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

    def _convert_series(self, series):
        """Convert values for use in SQL statements."""

        dtype = infer_dtype(series)

        if dtype in ["string", "categorical", "bytes"]:
            return series.map(self._quote)
        if dtype in ["datetime", "datetime64"]:
            return series.map(self._datetime)
        if dtype == "date":
            return series.map(self._date)

        # Leave as-is and hope for the best
        return series.astype(str)


class MSSQLGenerator(SQLGenerator):
    """Class for generating MS SQL Server compatible SQL."""

    @staticmethod
    def _id(identifier):
        return f"[{identifier}]"


class MySQLGenerator(SQLGenerator):
    """Class for generating MySQL compatible SQL."""

    @staticmethod
    def _id(identifier):
        return f"`{identifier}`"


class PostgreSQLGenerator(SQLGenerator):
    """Class for generating PostgreSQL compatible SQL."""

    @staticmethod
    def _id(identifier):
        return f'"{identifier}"'


class SQLiteGenerator(SQLGenerator):
    """Class for generating SQLite compatible SQL."""

    @staticmethod
    def _id(identifier):
        return f'"{identifier}"'
