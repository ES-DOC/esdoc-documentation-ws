"""
Data structure representing site level cache data.
"""

class CacheData():
    """
    Encapsulates site level cache data.
    """
    def __init__(self):
        """
        Constructor.
        """
        self._collections = {}
    

    def register(self, collection_key, collection):
        """
        Registers a collection with the cache.
        """
        self._collections[collection_key] = collection


    def get(self, collection_key, item_key=None, item_attribute=None):
        """
        Gets either a collection or an item from the cache.
        """
        collection = self._collections[collection_key]
        if item_key is None:
            return collection
        else:
            if isinstance(item_key, int):
                for item in collection:
                    if item.ID == item_key:
                        return item
            elif item_attribute is None:
                for item in collection:
                    if item.Name == item_key:
                        return item
            else:
                for item in collection:
                    if getattr(item, item_attribute) == item_key:
                        return item
        return None


    def get_project(self, code=None):
        """
        Returns either all projects or first project with matching code.
        """
        if code is None:
            return self.get('Project')
        elif isinstance(code, int):
            return self.get('Project', code)
        else:
            return self.get('Project', code.upper())


    def get_institute(self, code=None):
        """
        Returns either all institutea or first institute with matching code.
        """
        if code is None:
            return self.get('Institute')
        elif isinstance(code, int):
            return self.get('Institute', code)
        else:
            return self.get('Institute', code.upper())


    def get_cim_encoding(self, code=None):
        """
        Returns either all encodings or first encoding with matching code.
        """
        if code is None:
            return self.get('DocumentEncoding')
        elif isinstance(code, int):
            return self.get('DocumentEncoding', code)
        else:
            return self.get('DocumentEncoding', code.lower(), 'Encoding')


    def get_cim_schema(self, code=None):
        """
        Returns either all schemas or first schema with matching code.
        """
        if code is None:
            return self.get('DocumentSchema')
        elif isinstance(code, int):
            return self.get('DocumentSchema', code)
        else:
            return self.get('DocumentSchema', code.upper(), 'Version')


    def get_cim_language(self, code=None):
        """
        Returns either all languages or first language with matching code.
        """
        if code is None:
            return self.get('DocumentLanguage')
        elif isinstance(code, int):
            return self.get('DocumentLanguage', code)
        else:
            return self.get('DocumentLanguage', code.lower(), 'Code')
