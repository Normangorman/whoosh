"""
You want blobs? Cause we got em.
This engine uses a component-entity system, except entities are called blobs.
This is because blob is nice to type.
"""
import logging
from whoosh.components.base import BaseComponent
from whoosh.maths import Vec2f

logger = logging.getLogger(__name__)


class Blob:
    """
    You want a thing in your game? Well, you need a blob.
    """
    def __init__(self, name):
        self.name = name
        self.netid = 0
        self.tags = set()
        self.components = {} # maps component type to component instance

    def get_netid(self):
        """
        Returns the network ID of the blob, an int.
        """
        return self.netid

    def get_name(self):
        """
        Returns the name of the blob, a string.
        """
        return self.name

    def tag(self, tag):
        """
        Tags the blob with a descriptive tag (string).
        """
        if not isinstance(tag, basestring):
            raise ValueError("Given tag is not a string: {0}".format(tag))
        self.tags.add(tag)

    def has_tag(self, tag):
        """
        Returns True/False whether the blob has the given tag.
        """
        return tag in self.tags

    def add_component(self, component):
        """
        Adds a component to the blob.
        Components add functionality to the blob.
        See BaseComponent
        """
        if not isinstance(component, BaseComponent):
            raise ValueError("Component argument has the wrong type: {0}".format(component))
        self.components[type(component)] = component
        component._blob = self

    def get_component(self, component_type):
        """
        Gets the most recently added component of the given type.
        """
        return self.components.get(component_type)

    def has_component(self, component_type):
        """
        Returns True/False whether the blob has a component of the given type.
        """
        return self.get_component(component_type) != None

    def change_component(self, component_type, func):
        """
        Takes a component type and a function to use to modify the component.
        The most recently added component of that type will be passed as the first argument to the given function.
        """
        comp = self.get_component(component_type)
        if comp:
            func(comp)

    def itercomponents(self):
        """
        Returns an iterator across the blob's components.
        """
        return self.components.values()

    def debug(self):
        """
        Prints debug information about the blob.
        """
        logger.debug("Blob(name={0}, netid={1}, tags={2}, components={3})".format(
              self.name, self.netid, self.tags, self.components))

    def _set_netid(self, netid):
        """
        Sets the network ID of the blob.
        Only the engine core should really be doing this.
        """
        self.netid = netid
