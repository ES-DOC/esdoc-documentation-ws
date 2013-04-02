"""
Encapsulates entity conversion functions available to all Prodiguer entities.
"""
# Module imports.
import datetime
import simplejson

from sqlalchemy.orm import ColumnProperty, RelationshipProperty



class JSONEncoder(simplejson.JSONEncoder):
    """
    Extends simplejson to handle specific types.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat().replace('T', ' ')
        elif isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        else:
            return simplejson.JSONEncoder.default(self, obj)


class EntityConvertor(object):
    """
    Encapsulates all entity conversion functions.
    """

    @staticmethod
    def to_dict(target):
        """
        Returns a dictionary representation.
        """
        result = None
        iterator = None

        # Determine if target is a sequence.
        try:
            iterator = iter(target)
        except TypeError:
            pass

        # Convert.
        if iterator is None:
            result = target.as_dict()
        else:
            result = []
            for item in iterator:
                result.append(item.as_dict())

        return result


    @staticmethod
    def to_string(target):
        """
        Returns a string representation.
        """
        def get_rel_names(instance):
            """Returns list of entity relation properties."""
            return [p.key for p in instance.mapper.iterate_properties if isinstance(p, RelationshipProperty)]

        def get_rels(instance):
            """Returns dictionary of entity relations."""
            return dict([(name, getattr(instance, name)) for name in get_rel_names(instance)])

        def get_col_names(instance):
            """Returns list of entity column properties."""
            return [p.key for p in instance.mapper.iterate_properties if isinstance(p, ColumnProperty)]

        def get_cols(instance):
            """Returns dictinary of entity columns."""
            return dict([(name, getattr(instance, name)) for name in get_col_names(instance)])

        def att_as_string(att_name, att_value):
            """Returns the attribute name/value string representation."""
            result = " @{0}=".format(att_name)
            if att_name is None:
                result += "None"
            elif isinstance(att_value, datetime.datetime):
                result += str(att_value)
            else:
                result += repr(att_value)
            return result
        
        def class_as_string(name, id):
            """Returns the class name/value string representation."""
            return "<{0} ID={1}>".format(name, id)

        def rel_as_string(rel_name, rel_value):
            """Returns the relationship name/value string representation."""
            result = " R@{0}=".format(rel_name)
            if rel_value is None:
                result += "None"
            else:
                iterator = None
                try:
                    iterator = iter(rel_value)
                except TypeError:
                    result += class_as_string(rel_value.__class__.__name__, rel_value.ID)
                if iterator is not None:
                    result += "("
                    for item in iterator:
                        result += "{0}".format(item.ID)
                        result += ","
                    if len(rel_value) > 0:
                        result = result.rstrip(',')
                    result += ")"
            return result

        def as_string(instance):
            """Returns instance converted to a string."""
            # Class name + ID.
            result = "<{0}".format(instance.__class__.__name__)
            result += att_as_string("ID", instance.ID)

            # Property columns.
            cols = get_cols(instance)
            for col_name in cols:
                if col_name != "ID":
                    result += att_as_string(col_name, cols[col_name])

            # Relation columns.
            rels = get_rels(instance)
            for rel_name in rels:
                result += rel_as_string(rel_name, rels[rel_name])

            result += ">"
            return result

        result = None
        iterator = None

        # Determine if entity is a sequence.
        try:
            iterator = iter(target)
        except TypeError:
            pass

        # Convert.
        if iterator is None:
            result = as_string(target)
        else:
            result = []
            for item in iterator:
                result.append(as_string(item))

        return result
    

    @staticmethod
    def to_json(target):
        """
        Returns a json representation.
        """
        return JSONEncoder().encode(EntityConvertor.to_dict(target))