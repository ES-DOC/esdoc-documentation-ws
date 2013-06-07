"""Library exception class.

"""



class ESDOCAPIException(Exception):
    """Library exception class.

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
        return "ES-DOC API EXCEPTION : {0}".format(repr(self.message))
