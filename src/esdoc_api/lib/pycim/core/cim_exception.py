"""A CIM exception class.

"""

# Module exports.
__all__ = ['CIMException']



class CIMException(Exception):
    """A CIM meta-programming exception class.

    """

    def __init__(self, message):
        """Contructor.

        Keyword Arguments:
        self -- pointer to this object.

        """
        self.message = message


    def __str__(self):
        """Contructor.

        Keyword Arguments:
        self -- pointer to this object.

        """
        return "CIM EXCEPTION : {0}".format(repr(self.message))
