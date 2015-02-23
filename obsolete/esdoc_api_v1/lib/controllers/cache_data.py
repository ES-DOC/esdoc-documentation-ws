# -*- coding: utf-8 -*-

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


    def _get(self,
             collection_key,
             item_attribute,
             item_code,
             item_key_formatter):
        if item_code is None:
            return self.get(collection_key)
        elif isinstance(item_code, int):
            return self.get(collection_key, item_code)
        else:
            return self.get(collection_key, item_key_formatter(item_code), item_attribute)
    

    def register(self, collection_key, collection):
        """
        Registers a collection with the cache.
        """
        self._collections[collection_key] = collection


    def get(self, collection_key, item_key=None, item_attribute='Name'):
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
            else:
                for item in collection:
                    if getattr(item, item_attribute) == item_key:
                        return item
        return None


    def get_project(self, code=None):
        """
        Returns either all projects or first project with matching code.
        """
        return self._get('Project', 'Name', code, lambda key: key.upper())


    def get_institute(self, code=None):
        """
        Returns either all institutea or first institute with matching code.
        """
        return self._get('Institute', 'Name', code, lambda key: key.upper())
        

    def get_encoding(self, code=None):
        """Returns either all encodings or first encoding with matching code.
        
        """
        return self._get('DocumentEncoding', 'Encoding', code, lambda key: key.lower())


    def get_ontology(self, name, version):
        """Returns either all ontologies or first ontology with matching name/version.
        
        """
        for ontology in self.get('DocumentOntology'):
            if ontology.Name.upper() == name.upper() and \
               ontology.Version.upper() == version.upper() :
               return ontology
        return None


    def get_language(self, code=None):
        """Returns either all languages or first language with matching code.
        
        """
        return self._get('DocumentLanguage', 'Code', code, lambda key: key.lower())

