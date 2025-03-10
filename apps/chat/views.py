from django.db.models import Max
from drf_spectacular.utils import extend_schema
from rest_framework import (
    exceptions,
    filters,
    mixins,
    pagination,
    permissions,
    response,
    status,
    viewsets,
)

from apps.chat.models import ChatMessage, ChatRoom
from apps.chat.serializers import ChatMessageSerializer, ChatRoomSerializer


class ChatRoomViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]

    def get_queryset(self):
        return (
            ChatRoom.objects.prefetch_related("messages")
            .filter(user=self.request.user)
            .annotate(last_message_created_at=Max("messages__created_at"))
            .order_by("-last_message_created_at")
            .distinct()
        )

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            return response.Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChatMessageViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        if not ChatRoom.objects.filter(
            id=self.kwargs["room_pk"], user=self.request.user
        ).exists():
            raise exceptions.NotFound(detail="Room not found")
        return ChatMessage.objects.filter(room__id=self.kwargs["room_pk"]).order_by(
            "-id"
        )

    def perform_create(self, serializer) -> None:
        return serializer.save(room_id=self.kwargs["room_pk"])
