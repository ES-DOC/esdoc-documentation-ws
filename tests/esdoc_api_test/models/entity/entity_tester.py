"""
Encapsulates entity conversion functions available to all Metafor entities.
"""

# Module imports.
import unittest
from esdoc_api.lib.db.pgres.connect import *
from esdoc_api.models.entities.base_entity import ESDOCEntity
from esdoc_api.models.entities.entity_convertor import EntityConvertor
from cim_components_test.entity.entity_factory import EntityFactory



class EntityTester(object):
    """
    A set of tests to perform over entities.
    """

    @staticmethod
    def do_tests(entity_cls):
        """
        Performs the standard tests.
        """

        def do_factory_tests():
            """
            Factory related tests.
            """
            # Create instance.
            x = entity_cls()
            assert x is not None
            assert isinstance(x, ESDOCEntity) == True
            assert isinstance(x, entity_cls) == True

            # Create test instance.
            y = EntityFactory.create(entity_cls)
            assert y is not None
            assert isinstance(y, entity_cls) == True

            # Reset context.
            EntityFactory.clear_created()

            print "PASSED Entity Factory Test :: %s" % (entity_cls.__name__)
            
        
        def do_conversion_tests():
            """
            Conversion related tests - guarantees that different represenations are implemented.
            """
            # Create instance.
            x = EntityFactory.create(entity_cls)
            assert x is not None
            print "Created Test Instance :: {0}".format(repr(x))

            # Convert to string.
            s = EntityConvertor.to_string(x)
            assert s is not None

            # Convert to dictionary.
            d = EntityConvertor.to_dict(x)
            assert d is not None

            # Convert to json.
            j = EntityConvertor.to_json(x)
            assert j is not None

            # Reset context.
            EntityFactory.clear_created()

            print "PASSED Entity Repr Test :: %s" % (entity_cls.__name__)


        def do_db_tests():
            """
            Db related tests.
            """
            # Cache current count.
            count = entity_cls.get_count()
            print "Entity count = %d" % count

            # Create & reassert count.
            EntityFactory.create(entity_cls)
            session.commit()
            new_count = entity_cls.get_count()
            print "Entity count = %d" % new_count
            assert new_count == count + 1

            # Delete & reassert count.
            EntityFactory.delete_created()
            new_count = entity_cls.get_count()
            print "Entity count = %d" % new_count
            assert new_count == count

            print "PASSED Entity Db Test :: %s" % (entity_cls.__name__)


        do_factory_tests()
        do_conversion_tests()
        do_db_tests()
