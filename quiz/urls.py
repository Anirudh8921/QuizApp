from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, AnswerViewSet, UserQuizResultViewSet, UserAnswerViewSet

router = DefaultRouter()
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'user-quiz-results', UserQuizResultViewSet, basename='user-quiz-results')
router.register(r'user-answers', UserAnswerViewSet, basename='user-answers')


urlpatterns = [
    path('', include(router.urls)),
]
