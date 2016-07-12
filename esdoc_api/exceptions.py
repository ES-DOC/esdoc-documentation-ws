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