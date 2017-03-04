"""
The entire world in one python file.
"""
import pymunk
import pymunk.pyglet_util
import logging
import whoosh.blob
from whoosh.components.physics import PhysicsComponent

logger = logging.getLogger(__name__)


class GameWorld:
    """
    Everything in the world goes in here.
    """
    def __init__(self):
        self.blobs = []
        self.next_blob_netid = 0 # the next network id to assign a blob
        self.physics_world = pymunk.Space()
        self.physics_world.sleep_time_threshold = 0.3 # TODO: what does this do?
        self.physics_world.gravity = pymunk.vec2d.Vec2d(0.0, -1000.0)

    def update(self, dt):
        """
        Time is the most valuable currency so spend it wisely.
        #meaningfulquotes
        """
        logger.debug("GameWorld update called. {0} blobs. step {1}. bodies {2}, shapes {3}".format(
            len(self.blobs), dt, len(self.physics_world.bodies), len(self.physics_world.shapes)))
        self.physics_world.step(dt)

        # Pre tick
        for blob in self.blobs:
            for component in blob.itercomponents():
                component.on_pre_tick()
        # Tick
        for blob in self.blobs:
            for component in blob.itercomponents():
                component.on_tick()
        # Post tick
        for blob in self.blobs:
            for component in blob.itercomponents():
                component.on_post_tick()

    def add_blob(self, blob):
        """
        Lets a new blob into the world.
        """
        assert(isinstance(blob, whoosh.blob.Blob))
        self.blobs.append(blob)

        phys = blob.get_component(PhysicsComponent)
        if phys:
            self.physics_world.add(phys.body)
            for shape in phys.shapes:
                self.physics_world.add(shape)
        blob._set_netid(self._get_next_netid())

    def _get_next_netid(self):
        """
        Returns a network ID that can be used for a new blob.
        """
        self.next_blob_netid += 1
        return self.next_blob_netid
