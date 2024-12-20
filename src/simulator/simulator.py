from abc import ABC, abstractmethod


class Simulator(ABC):
    """
    This guy is the main part simulating life
    """
    @abstractmethod
    def run(self):
        """Method that must be implemented by all subclasses."""
        pass
