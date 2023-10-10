from abc import ABC

from app.kernel.domain.repository import BaseRepository


class MemoryCacheRepositoryInterface(BaseRepository, ABC):
    """Interface for cache repository"""
