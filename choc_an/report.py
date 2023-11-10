from abc import ABC, abstractmethod


class Report(ABC):
    @abstractmethod
    def output(self) -> str:
        pass
