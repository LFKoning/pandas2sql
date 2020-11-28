"""Module for table constraint classes."""


class PrimaryKey:
    """
    Implements primary key constraint.

    Parameters
    ----------
    columns : Union[str, list[str]]
        Column(s) of the primary key constraint.
    """

    def __init__(self, columns):

        if isinstance(columns, str):
            columns = [columns]

        self.columns = columns

    def make(self, id_fn):
        """
        Creates string representation for the primary key constraint.

        Parameters
        ----------
        id_fn : Callable
            Function to escape / quote indentifiers.

        Returns
        -------
        str
            String representation of the constraint.
        """
        # Construct parts and escape IDs
        name = id_fn("PK_" + "_".join(self.columns))
        columns = ", ".join([id_fn(col) for col in self.columns])

        return f"CONSTRAINT {name} PRIMARY KEY ({columns})"


class ForeignKey:
    """
    Implements foreign key constraint.

    Parameters
    ----------
    columns : Union[str, list[str]]
        Column(s) of the foreign key constraint.
    ref_table : str
        Table the constraint refers to.
    ref_columns : Union[str, list[str]]
        Columns the foreign key refers to.
    on_delete : Optional[str]
        Action to perform when records are deleted.
        Valid choices are: "CASCADE".
    on_update : Optional[str]
        Action to perform when records are updated, defaults to None.
        Valid choices are: "CASCADE", "NO ACTION", "SET NULL", "SET DEFAULT".
    """

    # pylint: disable=too-many-arguments, bad-continuation
    def __init__(self, columns, ref_table, ref_columns, delete=None, update=None):

        if isinstance(columns, str):
            columns = [columns]
        if isinstance(ref_columns, str):
            ref_columns = [ref_columns]

        self.columns = columns
        self.ref_table = ref_table
        self.ref_columns = ref_columns
        self.delete = delete
        self.update = update

    def make(self, id_fn):
        """
        Creates string representation for the foreign key constraint.

        Parameters
        ----------
        id_fn : Callable
            Function to escape / quote indentifiers.

        Returns
        -------
        str
            String representation of the constraint.
        """

        # Construct parts and escape IDs
        name = id_fn("FK_" + "_".join(self.columns))
        columns = ", ".join([id_fn(col) for col in self.columns])
        ref_table = id_fn(self.ref_table)
        ref_columns = ", ".join([id_fn(col) for col in self.columns])

        constraint = (
            f"CONSTRAINT {name} FOREIGN KEY ({columns}) "
            f"REFERENCES {ref_table}({ref_columns})"
        )

        if self.delete:
            constraint += f" ON DELETE {self.delete.upper()}"
        if self.update:
            constraint += f" ON UPDATE {self.update.upper()}"

        return constraint
