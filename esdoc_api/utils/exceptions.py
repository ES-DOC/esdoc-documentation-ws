# -*- coding: utf-8 -*-
"""
.. module:: exceptions.py
   :platform: Unix
   :synopsis: Exceptions raised across web-service.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import inspect



class API_Exception(Exception):
    """API exception class.

    """

    def __init__(self, msg):
        """Contructor.

        :param msg: Exception message.
        :type msg: str

        """
        self.message = msg() if inspect.isfunction(msg) else str(msg)


    def __str__(self):
        """Returns a string representation.

        """
        return "ES-DOC API EXCEPTION : {0}".format(repr(self.message))



class RequestValidationException(Exception):
    """Base class for request validation exceptions.

    """
    pass


class SecurityError(RequestValidationException):
    """Raised if a security issue arises.

    """
    def __init__(self, msg):
        """Instance constructor.

        """
        super(SecurityError, self).__init__(
            "SECURITY EXCEPTION :: {}".format(msg)
            )


class InvalidJSONSchemaError(RequestValidationException):
    """Raised if the submitted request data is invalid according to a JSON schema.

    """
    def __init__(self, json_errors):
        """Instance constructor.

        """
        super(InvalidJSONSchemaError, self).__init__(
            'ISSUE HAS INVALID JSON SCHEMA: \n{}'.format(json_errors))


class DocumentDecodingException(RequestValidationException):
    """Raised if the submitted request body payload cannot be decoded.

    """
    def __init__(self):
        """Instance constructor.

        """
        super(DocumentDecodingException, self).__init__(
            "DOCUMENT DECODING FAILURE"
            )


class DocumentInvalidException(RequestValidationException):
    """Raised if the submitted document is invalid.

    """
    def __init__(self, msg=None):
        """Instance constructor.

        """
        super(DocumentInvalidException, self).__init__(
            "DOCUMENT IS INVALID: {}".format(msg) if msg else "DOCUMENT IS INVALID"
            )


class DocumentPublishedException(RequestValidationException):
    """Raised if the submitted document has already been published.

    """
    def __init__(self, msg=None):
        """Instance constructor.

        """
        super(DocumentPublishedException, self).__init__(
            "DOCUMENT HAS ALREADY BEEN PUBLISHED, REPUBLISH INSTEAD"
            )
