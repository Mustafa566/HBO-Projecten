from django.contrib.auth.models import User
from rest_framework import serializers
from .models import OpenQ, MultipleChoiceQ, Survey


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


# Question serializers inspired by
# https://blog.logrocket.com/using-react-django-create-app-tutorial/
class OpenQSerializer(serializers.ModelSerializer):
    is_hidden = serializers.BooleanField()

    class Meta:
        model = OpenQ
        fields = (
            'question_id',
            'question_text',
            'is_hidden',
        )


class MultipleChoiceQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQ
        fields = (
            'mc_id',
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'is_hidden',
        )


class SurveySerializer(serializers.ModelSerializer):
    open_q = serializers.PrimaryKeyRelatedField(many=True, queryset=OpenQ.objects.all())
    mc_q = serializers.PrimaryKeyRelatedField(many=True, queryset=MultipleChoiceQ.objects.all())

    class Meta:
        model = Survey
        fields = (
            'survey_id',
            'admin',
            'title',
            'description',
            'is_anonymous',
            'date_sent',
            'open_q',
            'mc_q',
            'url',
        )

    def create(self, validated_data):
        open_q_data = validated_data.pop('open_q')
        mc_q_data = validated_data.pop('mc_q')
        survey = Survey.objects.create(**validated_data)

        for question in open_q_data:
            survey.open_q.add(question)

        for question in mc_q_data:
            survey.mc_q.add(question)

        return survey


