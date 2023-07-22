
from django.contrib import admin
from django.urls import path
from ccforms import views
from ccforms.views import LoginView, SurveyDetailView, UserList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', UserList.as_view()),
    path('api/currentUser/', views.current_user),
    path('api/open_questions/', views.open_q_list),
    path('api/open_questions/<int:pk>/', views.open_q_detail, name='open_q_detail'),
    path('api/open_questions/<int:pk>/hide/', views.hide_open_q),
    path('api/open_questions/<int:pk>/edit/', views.edit_open_q),
    path('api/mc_questions/', views.mc_q_list),
    path('api/mc_questions/<int:pk>/hide/', views.hide_mc_q),
    path('api/surveys/', views.survey_list),
    path('api/surveys/<int:pk>/', views.survey_detail),
    path('api/register/', views.register),
    path('api/login/', LoginView.as_view()),
    path('api/survey/<int:pk>/', SurveyDetailView.as_view(), name='survey-detail'),
    path('api/openQuestions/<int:pk>/', views.open_question_detail, name='open_question_detail'),
    path('api/multipleChoiceQuestions/<int:pk>/', views.multiple_choice_question_detail, name='multiple_choice_question_detail'),
    path('api/PostRespond/', views.post_respond, name='post_respond'),
    path('api/surveys/count/', views.count_surveys, name='survey_count'),
    path('api/counters/', views.counters),
]
