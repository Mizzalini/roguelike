from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class BaseComponent:
    """
    Base class for components.
    """
    entity: Entity  # The entity this component is attached to

    @property
    def engine(self) -> Engine:
        """
        Returns the engine this component is attached to.
        """
        return self.entity.game_map.engine
