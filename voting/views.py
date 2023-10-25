from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from voting.models import Voting
from voting.serializers import VotingSerializer


class VotingViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VotingSerializer
    queryset = Voting.objects.get_votes_for_today_menus()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
