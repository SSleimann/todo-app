from app.modules.todo.infrastructure.mapper import TaskMapper
from app.modules.todo.domain.entities import TaskEntity
from app.modules.todo.infrastructure.models import TaskModel
from app.modules.todo.domain.value_objects import StatusValue

task1 = TaskEntity(
    id=TaskEntity.next_id(),
    title="Test Title 1",
    description="Task1",
    status=StatusValue.DONE,
    user_id=TaskEntity.next_id(),
)


mapper = TaskMapper()


def test_task_to_model():
    instance = mapper.entity_to_model(task1)

    assert instance.id == task1.id
    assert instance.title == task1.title
    assert instance.description == task1.description
    assert instance.status == task1.status
    assert instance.user_id == task1.user_id


def test_model_to_entity():
    instance = TaskModel(
        id=TaskEntity.next_id(),
        title="Test Title 1",
        description="Task1",
        status=StatusValue.DONE,
        user_id=TaskEntity.next_id(),
    )
    

    entity = mapper.model_to_entity(instance)

    assert entity.id == instance.id
    assert entity.title == instance.title
    assert entity.description == instance.description
    assert entity.status == instance.status
    assert entity.user_id == instance.user_id
