from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Quiz, Question, Answer, UserQuizResult, UserAnswer
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, UserQuizResultSerializer, UserAnswerSerializer
from rest_framework import status, parsers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework_simplejwt.authentication import JWTAuthentication

class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

# Retrieve a quiz with its questions
class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

# Submit quiz answers
class SubmitQuizView(generics.CreateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        quiz_id = kwargs.get('quiz_id')
        quiz = get_object_or_404(Quiz, id=quiz_id)

        submitted_answers = request.data.get("answers", [])  # Expecting a list of answers
        score = 0
        total_questions = quiz.questions.count()

        # Store user answers and calculate score
        for answer_data in submitted_answers:
            question_id = answer_data.get("question_id")
            selected_answer_id = answer_data.get("selected_answer_id")

            question = get_object_or_404(Question, id=question_id, quiz=quiz)
            selected_answer = get_object_or_404(Answer, id=selected_answer_id, question=question)

            # Save user's answer
            UserAnswer.objects.create(user=user, question=question, selected_answer=selected_answer)

            # Check if the answer is correct
            if selected_answer.is_correct:
                score += 1

        # Save final quiz result
        result = UserQuizResult.objects.create(user=user, quiz=quiz, score=score, time_taken=request.data.get("time_taken", 0))

        return Response({"message": "Quiz submitted successfully", "score": score, "total_questions": total_questions}, status=status.HTTP_201_CREATED)


class UserQuizResultViewSet(ModelViewSet):
    queryset = UserQuizResult.objects.all()
    serializer_class = UserQuizResultSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class UserAnswerViewSet(ModelViewSet):
    queryset = UserQuizResult.objects.all()
    serializer_class = UserAnswerSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]    

    def create(self, request, *args, **kwargs):
        score = request.data.get('score')
        quiz_id = request.data.get('quiz_id')
        time_taken = request.data.get('time_taken')
        user = request.user  # Get the authenticated user

        # Create UserQuizResult
        user_quiz_result = UserQuizResult.objects.create(
            quiz_id=quiz_id,
            score=score,
            time_taken=time_taken
        )

        # Create UserAnswer instances
        answers = request.data.get('answers', [])
        for answer_data in answers:
            question_id = answer_data.get('question_id')
            selected_answer_id = answer_data.get('selected_answer_id')

            # Create UserAnswer instance
            UserAnswer.objects.create(
                user=user,
                question_id=question_id,
                selected_answer_id=selected_answer_id
            )
        serializer = self.get_serializer(user_quiz_result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class QuizAnalyticsView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        analytics_data = Quiz.objects.annotate(
            avg_score=Avg('userquizresult__score'),
            total_attempts=Count('userquizresult')
        ).values('title', 'avg_score', 'total_attempts')

        return Response({"analytics": list(analytics_data)})   