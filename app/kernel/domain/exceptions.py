class EntityNotFoundException(Exception):
    def __init__(self) -> None:
        self.message = "Entity not found"
