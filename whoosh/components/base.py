import abc
from whoosh.engine.hooker import EngineHooker

class BaseComponent(EngineHooker):
    """
    Components are things attached to blobs that do stuff or hold information.
    All components should derive from this base class.
    Components work by implementing various hooks that the engine calls on components, such as on_tick - which is
    called every tick.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        EngineHooker.__init__(self)
        self.properties = {} # it is useful for many reasons for components to have a set of key-value pairs
        self._blob = None

    def on_add_to_blob(self, blob):
        """
        Called once when the component is added to a blob
        """
        pass

    def on_die(self):
        """
        Called when the blob dies.
        """
        pass

    def on_collision_begin(self, arbiter, data):
        """
        Called when the blob begins to collide with something
        """
        pass

    def on_collision_separate(self, arbiter, data):
        """
        Called when the blob finishes colliding with something
        """
        pass

    def set_prop(self, prop_name, prop_val):
        """
        Sets a property on the component with the given name and value.
        """
        self.properties[prop_name] = prop_val

    def get_prop(self, prop_name):
        """
        Returns the value of the property on the component if it exists, else None
        """
        return self.properties.get(prop_name)

    def change_prop(self, prop_name, func):
        """
        Alters a property using the given function.
        The function should take one argument (the property value) and return the changed value.
        """
        assert(callable(func))
        val = self.get_prop(prop_name)
        if not val:
            raise ValueError("Component has no property {0}".format(prop_name))
        else:
            self.set_prop(prop_name, func(val))

    def has_prop(self, prop_name):
        """
        Returns True/False whether the component has the given property.
        """
        return prop_name in self.properties

    def get_blob(self):
        """
        Returns the Blob which this component is attached to, if there is one.
        self._blob should be set by Blob.add_component
        """
        return self._blob
