"""
Metafor entity factory used for testing purposes.
"""

# Module imports.
import uuid
import random
import datetime

from esdoc_api.lib.db.pgres.connect import *



# Collection of created entities.
_created_entites = []

# Set of handlers for hydrating entity instances.
_hydration_handlers = {}


def _hydrate_IngestState(instance):
    """
    Hydrates an instance for test purposes.
    """
    instance.Name = str(uuid.uuid1())[:16]
    instance.Description = "Test execution state."
    instance.Code = random.randint(0, 9999999)
_hydration_handlers[IngestState] = _hydrate_IngestState


def _hydrate_Institute(instance):
    """
    Hydrates an instance for test purposes.
    """
    instance.Name = str(uuid.uuid1())[:16]
    instance.LongName = u"BCC"
    instance.CountryCode = u"FR"
    instance.URL = u"http://www.ipsl.fr/"
_hydration_handlers[Institute] = _hydrate_Institute


def _hydrate_IngestHistory(instance):
    """
    Hydrates an instance for test purposes.
    """
    instance.Count = 100
    instance.TimeInMS = 10000
    instance.Registration = ir
    instance.State = EntityFactory.create(IngestState)
    instance.StartDateTime = datetime.datetime.now()
    instance.EndDateTime = datetime.datetime.now()
_hydration_handlers[IngestHistory] = _hydrate_IngestHistory


def _hydrate_IngestSource(instance):
    """
    Hydrates an instance for test purposes.
    """
    instance.Name = str(uuid.uuid1())[:16]
    instance.Description = "Test Ingest Source"
_hydration_handlers[IngestSource] = _hydrate_IngestSource


def _hydrate_IngestRegistration(instance):
    """
    Hydrates an instance for test purposes.
    """
    instance.IsActive = False
    instance.ContactName = str(uuid.uuid1())[:32]
    instance.ContactEmail = str(uuid.uuid1())[:32]
    instance.ContactTelephone = str(uuid.uuid1())[:32]
    instance.IngestURL = str(uuid.uuid1())[:32]
    instance.Institute = EntityFactory.create(Institute)
    instance.IngestSource = EntityFactory.create(IngestSource)
_hydration_handlers[IngestRegistration] = _hydrate_IngestRegistration


class EntityFactory(object):
    """
    Returns test instances of entites.
    """
    @staticmethod
    def clear_created():
        """
        Deletes all previously created entities.
        """
        print "Entity Factory clearing instance collection"
        session.rollback()
        del(_created_entites[:])


    @staticmethod
    def delete_created():
        """
        Deletes all previously created entities.
        """
        print "Entity Factory deleting instance collection (%d instances)" % len(_created_entites)

        # Delete in reverse order of creation.
        _created_entites.reverse()
        while len(_created_entites) > 0:
            instance = _created_entites.pop()
            print "Entity Factory deleting instance of %s" % instance.__class__.__name__
            instance.delete()
            session.commit()
            print "Entity Factory deleted instance of %s" % instance.__class__.__name__


    @staticmethod
    def create(entity_cls):
        """
        Creates & returns an entity for testing purposes.
        """
        print "Entity Factory creating instance of %s" % entity_cls.__name__

        # Create & cache.
        instance = entity_cls()
        _created_entites.append(instance)

        # Hydrate accordingly.
        try:
            hydration = _hydration_handlers[entity_cls]
        except KeyError:
            _created_entites.pop()
            raise TypeError("Entity Factory does not support passed entity type.")
        hydration(instance)

        return instance