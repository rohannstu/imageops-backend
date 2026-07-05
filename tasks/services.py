from datetime import date
from .models import Task


class TaskService:
    @staticmethod
    def get_tasks_for_date(user, target_date):
        return Task.objects.filter(user=user, due_date=target_date)

    @staticmethod
    def create_task(user, data):
        if not data.get('title'):
            raise ValueError("Task title is required")
        if not data.get('due_date'):
            raise ValueError("Task due date is required")

        return Task.objects.create(
            user=user,
            title=data['title'],
            description=data.get('description', ''),
            status=data.get('status', Task.Status.TODO),
            priority=data.get('priority', Task.Priority.MEDIUM),
            due_date=data['due_date'],
            tags=data.get('tags', []),
        )

    @staticmethod
    def update_task_status(task, new_status):
        valid_statuses = [choice[0] for choice in Task.Status.choices]
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status: {new_status}")

        task.status = new_status
        task.save(update_fields=['status', 'updated_at'])
        return task