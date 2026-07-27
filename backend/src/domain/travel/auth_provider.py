from abc import ABC, abstractmethod

from src.domain.travel.auth import AccessToken


class AuthProvider(ABC):

    @abstractmethod
    async def authenticate(self) -> AccessToken:
        pass