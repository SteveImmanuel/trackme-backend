from abc import ABC, abstractmethod
from typing import Dict


class BaseModel(ABC):

    @abstractmethod
    def to_dict(self) -> Dict:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def from_dict(data) -> 'BaseModel':
        raise NotImplementedError