from django.urls import path

from voting.views import VotingViewSet

app_name = "voting"

urlpatterns = [
    path("create/", VotingViewSet.as_view({'post': 'create'}), name="create_voting"),
    path("today/", VotingViewSet.as_view({'get': 'list'}), name="voting_list"),
]

