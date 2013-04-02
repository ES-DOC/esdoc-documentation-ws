"""
Utility functions used during setup process.
"""

# Module imports.


def get_rows(text, split='|'):
    """Parses incoming data and yields each row as an array of values.

    """
    for row in [line.split(split) for line in text.splitlines()]:
        for i in range(len(row)):
            row[i] = row[i].strip()
        yield row
