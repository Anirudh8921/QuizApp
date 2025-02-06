from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, AnswerViewSet, SubmitQuizViewSet, UserQuizResultViewSet, LeaderboardViewSet, QuizAnalyticsView 

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'quizzes/(?P<quiz_id>[^/.]+)/submit', SubmitQuizViewSet, basename='submit-quiz')
router.register(r'user-quiz-results', UserQuizResultViewSet, basename='user-quiz-results')
# router.register(r'user-answers', UserAnswerViewSet, basename='user-answers')
router.register(r'leaderboard', LeaderboardViewSet)
router.register(r'quiz-analytics', QuizAnalyticsView, basename='quiz-analytics')

urlpatterns = [
    path('', include(router.urls)),
]
