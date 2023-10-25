from rest_framework import serializers

from voting.models import Voting


class VotingSerializer(serializers.ModelSerializer):
    restaurant = serializers.IntegerField(source='menu.restaurant_id', read_only=True)

    class Meta:
        model = Voting
        fields = '__all__'
        read_only_fields = ['user']
