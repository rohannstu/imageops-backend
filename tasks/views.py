from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer
from .services import TaskService


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(due_date=date_param)
        return queryset

    def perform_create(self, serializer):
        data = serializer.validated_data
        TaskService.create_task(self.request.user, data)

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        new_status = request.data.get('status')

        try:
            TaskService.update_task_status(task, new_status)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(TaskSerializer(task).data)