from abc import ABC, abstractmethod
from typing import Dict


class BaseSchema(ABC):

    @abstractmethod
    def to_dict(self) -> Dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def from_dict(data) -> 'BaseSchema':
        raise NotImplementedError