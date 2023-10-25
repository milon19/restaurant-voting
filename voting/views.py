from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from voting.models import Voting, VotingResult
from restaurant.models import Restaurant
from restaurant.serializers import RestaurantSerializer
from voting.serializers import VotingSerializer


class VotingViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = VotingSerializer
    queryset = Voting.objects.get_votes_for_today_menus()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VotingResultAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get_winners_to_exclude():
        today = timezone.now().date()

        window_start = today - timedelta(days=3)
        window_end = today

        winners_in_window = (
            VotingResult.objects
            .filter(date__range=(window_start, window_end))
            .values('winner')
            .annotate(wins_count=Count('winner'))
            .filter(wins_count=3)
        )

        winners_to_exclude = [winner['winner'] for winner in winners_in_window]

        return winners_to_exclude

    @staticmethod
    def get_restaurant_details(restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        serializer = RestaurantSerializer(restaurant)
        return serializer.data

    def get(self, request):
        todays_result = VotingResult.objects.filter(date=timezone.now().date())
        if todays_result.exists():
            data = self.get_restaurant_details(todays_result.first().winner_id)
            return Response(data, status=status.HTTP_200_OK)

        else:
            restaurants_with_votes = Voting.objects.get_restaurants_with_votes_today()
            result = {}
            for restaurant in restaurants_with_votes:
                result[restaurant['restaurant_id']] = restaurant['total_votes']

            winners_to_exclude = self.get_winners_to_exclude()
            result_after_exclude = set(result.keys()) - set(winners_to_exclude)
            final_result = result_after_exclude.pop()
            if not final_result:
                final_result = list(result.keys())[0]
            VotingResult.objects.create(date=timezone.now().date(), winner_id=final_result, total_vote=result[final_result])
            data = self.get_restaurant_details(final_result)
            return Response(data, status=status.HTTP_200_OK)
