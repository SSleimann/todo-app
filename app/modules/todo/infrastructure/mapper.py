from app.kernel.infrastructure.mapper import BaseMapper

from app.modules.todo.domain.entities import TaskEntity
from app.modules.todo.infrastructure.models import TaskModel


class TaskMapper(BaseMapper):
    def model_to_entity(self, instance: TaskModel) -> TaskEntity:
        return TaskEntity(
            id=instance.id,
            title=instance.title,
            description=instance.description,
            status=instance.status,
            user_id=instance.user_id,
        )

    def entity_to_model(self, entity: TaskEntity) -> TaskModel:
        return TaskModel(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            status=entity.status,
            user_id=entity.user_id,
        )
