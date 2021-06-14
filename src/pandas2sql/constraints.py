"""Module for table constraint classes."""

from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Union


class Constraint(ABC):
    """Constraint abstract base class."""

    @abstractmethod
    def make(self, id_fn: Callable) -> str:
        """Creates string representation for the primary key constraint.

        Parameters
        ----------
        id_fn : Callable
            Function to escape / quote indentifiers.

        Returns
        -------
        str
            String representation of the constraint.
        """


class PrimaryKey(Constraint):
    """
    Implements primary key constraint.

    Parameters
    ----------
    columns : Union[list[str], str]
        Column(s) of the primary key constraint.
    """

    def __init__(self, columns: Union[List[str], str]) -> None:

        if isinstance(columns, str):
            columns = [columns]

        self.columns = columns

    def make(self, id_fn: Callable) -> str:
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


class ForeignKey(Constraint):
    """
    Implements foreign key constraint.

    Parameters
    ----------
    columns : Union[List[str], str]
        Column(s) of the foreign key constraint.
    ref_table : str
        Table the constraint refers to.
    ref_columns : Union[List[str], str]
        Columns the foreign key refers to.
    delete : Optional[str]
        Action to perform when records are deleted.
        Valid choices are: "CASCADE", "NO ACTION", "SET NULL", "SET DEFAULT".
    update : Optional[str]
        Action to perform when records are updated, defaults to None.
        Valid choices are: "CASCADE", "NO ACTION", "SET NULL", "SET DEFAULT".
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        columns: Union[List[str], str],
        ref_table: str,
        ref_columns: Union[List[str], str],
        delete: Optional[str] = None,
        update: Optional[str] = None,
    ) -> None:

        if isinstance(columns, str):
            columns = [columns]
        if isinstance(ref_columns, str):
            ref_columns = [ref_columns]

        valid = "NO ACTION", "RESTRICT", "CASCADE", "SET NULL", "SET DEFAULT"
        if delete and delete.upper() not in valid:
            raise ValueError(
                f"Invalid delete action {delete}, choose one of: {', '.join(valid)}"
            )
        if update and update.upper() not in valid:
            raise ValueError(
                f"Invalid update action {update}, choose one of:  {', '.join(valid)}"
            )

        self.columns = columns
        self.ref_table = ref_table
        self.ref_columns = ref_columns
        self.delete = delete
        self.update = update

    def make(self, id_fn: Callable) -> str:
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
