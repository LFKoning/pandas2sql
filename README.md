# Pandas2SQL

## Goal

Easily generate SQL scripts for exporting data from pandas DataFrames.

## Installation

```bash
pip install pandas2sql
```

## Usage

First create a generator object for the appropriate database back-end lise so:

```python
from pandas2sql.generators import SQLiteGenerator

generator = SQLiteGenerator()
```

Then you can easily create a SQL schema definition like so:

```python
import pandas as pd

df = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "name": ["Jane", "John", "Kate", "Bob"],
    "age": [25, 32, 54, 42],
})

# Creates schema for the "Persons" table.
print(gen.generate_schema(df, "Persons"))
```

Executing this code returns the following SQL schema:

```SQL
CREATE TABLE "Persons" (
  "id" INTEGER,
  "name" TEXT,
  "age" INTEGER
);
```

Finally, if you want to create INSERT statements for the data, use:

```Python
# Create INSERT statements for the data
for _ in gen.generate_inserts(df, "Persons"):
    print(_)
```

This will return a list of (batched) INSTERT statements as strings, for example:

```sql
INSERT INTO "Persons" ("id", "name", "age")
VALUES
  (1, 'Jane', 25),
  (2, 'John', 32),
  (3, 'Kate', 54),
  (4, 'Bob', 42)
;
```
