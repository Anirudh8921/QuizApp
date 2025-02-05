from rest_framework import serializers
from .models import Quiz, Question, Answer, UserQuizResult, UserAnswer



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = '__all__'        

class UserQuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizResult
        fields = '__all__'

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'    

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'            