from abc import ABC, abstractmethod


class SimulateJob(ABC):
    """
    This guy is connecting all packages and shows you desired result
    """
    @abstractmethod
    def run(self):
        """Method that must be implemented by all subclasses."""
        pass
