from abc import ABC, abstractmethod
from typing import Dict


class BaseSchema(ABC):

    @abstractmethod
    def to_dict(self) -> Dict:
        raise NotImplementedError

    @abstractmethod
    @staticmethod
    def from_dict(data) -> 'BaseSchema':
        raise NotImplementedError

    @abstractmethod
    def validate_params(self, data: Dict) -> bool:
        raise NotImplementedError