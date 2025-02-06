from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .models import Quiz, Question, Answer, UserQuizResult, UserAnswer
from .serializers import QuizSerializer, QuestionSerializer, AnswerSerializer, UserQuizResultSerializer, UserAnswerSerializer
from rest_framework import status, parsers
from django.db.models import Avg, Max, Count
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import permissions, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema

class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of quizzes",
        responses={200: QuizSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=QuizSerializer,
        responses={201: QuizSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT', 'DELETE']:  # Only allow admins to modify
    #         return [permission.IsAdminUser()]
    #     # return [permission_classes()]
    #     return super().get_permissions()

class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of questions",
        responses={200: QuestionSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=QuestionSerializer,
        responses={201: QuestionSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a list of answers",
        responses={200: AnswerSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request , *args, **kwargs)

    @swagger_auto_schema(
        request_body=AnswerSerializer,
        responses={201: AnswerSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# class UserQuizResultListCreateViewSet(ModelViewSet):
#     queryset = UserQuizResult.objects.all()
#     serializer_class = UserQuizResultSerializer
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return UserQuizResult.objects.filter(user=self.request.user)    


# Retrieve a quiz with its questions
# class QuizDetailViewSet(ModelViewSet):
#     queryset = Quiz.objects.all()
#     serializer_class = QuizSerializer
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

# Submit quiz answers
class SubmitQuizViewSet(ModelViewSet):
    serializer_class = UserAnswerSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=UserAnswerSerializer(many=True),
        responses={201: UserQuizResultSerializer},
    )
    def post(self, request, quiz_id, *args, **kwargs):
        user = request.user
        quiz = get_object_or_404(Quiz, id=quiz_id)

        submitted_answers = request.data.get("answers", [])
        score = 0

        for answer_data in submitted_answers:
            question_id = answer_data.get("question_id")
            selected_answer_id = answer_data.get("selected_answer_id")

            question = get_object_or_404(Question, id=question_id, quiz=quiz)
            selected_answer = get_object_or_404(Answer, id=selected_answer_id, question=question)

            UserAnswer.objects.create(user=user, question=question, selected_answer=selected_answer)

            if selected_answer.is_correct:
                score += 1

        result = UserQuizResult.objects.create(user=user, quiz=quiz, score=score, time_taken=request.data.get("time_taken", 0))

        return Response({"message": "Quiz submitted successfully", "score": score}, status=status.HTTP_201_CREATED)  

# Get a user's past results
class UserQuizResultViewSet(ModelViewSet):
    queryset = UserQuizResult.objects.all()
    serializer_class = UserQuizResultSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve a user's quiz results",
        responses={200: UserQuizResultSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

# class UserAnswerViewSet(ModelViewSet):
#     queryset = UserQuizResult.objects.all()
#     serializer_class = UserAnswerSerializer
#     parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]    

#     def create(self, request, *args, **kwargs):
#         score = request.data.get('score')
#         quiz_id = request.data.get('quiz_id')
#         time_taken = request.data.get('time_taken')
#         user = request.user  # Get the authenticated user

#         # Create UserQuizResult
#         user_quiz_result = UserQuizResult.objects.create(
#             quiz_id=quiz_id,
#             score=score,
#             time_taken=time_taken
#         )

#         # Create UserAnswer instances
#         answers = request.data.get('answers', [])
#         for answer_data in answers:
#             question_id = answer_data.get('question_id')
#             selected_answer_id = answer_data.get('selected_answer_id')

#             # Create UserAnswer instance
#             UserAnswer.objects.create(
#                 user=user,
#                 question_id=question_id,
#                 selected_answer_id=selected_answer_id
#             )
#         serializer = self.get_serializer(user_quiz_result)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
        
class LeaderboardViewSet(ModelViewSet):
    queryset = UserQuizResult.objects.all().order_by('-score')
    serializer_class = UserQuizResultSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve the leaderboard",
        responses={200: UserQuizResultSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # def get_queryset(self):
    #     return (
    #         UserQuizResult.objects
    #         .values('user__username')
    #         .annotate(total_score=Max('score'), attempts=Count('id'))
    #         .order_by('-total_score', 'attempts')
    #     )        

class QuizAnalyticsView(ModelViewSet):
    queryset = UserQuizResult.objects.all().order_by('-score')
    serializer_class = UserQuizResultSerializer
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.FileUploadParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve quiz analytics data",
        responses={200: UserQuizResultSerializer(many=True)},
    )

    def get(self, request):
        analytics_data = Quiz.objects.annotate(
            avg_score=Avg('userquizresult__score'),
            total_attempts=Count('userquizresult')
        ).values('title', 'avg_score', 'total_attempts')

        return Response({"analytics": list(analytics_data)})  

