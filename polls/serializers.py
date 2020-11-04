from rest_framework import serializers
from users.serializers import UserSerializer

from polls.models import Choice, Question


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text', 'votes', 'created_at',)


class QuestionListSerializer(serializers.ModelSerializer):
    choices = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date', 'choices',)


class QuestionDetailSerializer(serializers.ModelSerializer):
    choices = serializers.StringRelatedField(many=True)
    created_by = UserSerializer()

    class Meta:
        model = Question
        fields = ('id', 'question_text', 'pub_date', 'created_by', 'choices',)
