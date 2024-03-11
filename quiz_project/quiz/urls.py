from django.urls import path
from .views import quiz_detail_view, result_view, quiz_index_view, signup, user_login, custom_logout


urlpatterns = [
    path('', signup, name='signup'),
    path('login', user_login, name='login'),
    path('quiz/quizIndex', quiz_index_view, name='quiz_index'),  
    path('<int:quiz_id>/', quiz_detail_view, name='quiz_detail_view'),
    path('<int:quiz_id>/result/', result_view, name='result_view'),
    path('logout/', custom_logout, name='logout'),
]
