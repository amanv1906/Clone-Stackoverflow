"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from stackoverflow import views

urlpatterns = [
    # authentication
    path('api/signup', views.Signup.as_view()),
    path('api/authenticate', views.Authenticate.as_view()),

    # users
    path('api/users', views.ListUser.as_view()),
    path('api/users/<str:username>', views.UserSearch.as_view()),
    path('api/user/<str:username>', views.UserDetail.as_view()),

    # questions
    path('api/question', views.QuestionView.as_view()),
    path('api/question/<int:q_id>', views.QuestionDetailView.as_view()),
    path('api/questions/<str:tag>', views.QuestionTag.as_view()),
    path('api/question/user/<str:name>', views.UserQuestion.as_view()),
    path('api/questions', views.QuestionPost.as_view()),

    # tags
    path('api/tags', views.TagsView.as_view()),
    path('api/tags/populertags', views.PopularTags.as_view()),
    path('api/tags/<str:tag>', views.TagSearchView.as_view()),

    # Answer
    path('api/answer/<int:question_id>', views.AnswerView.as_view()),
    path('api/answer/<int:question_id>/<int:answer_id>',
         views.AnswerView.as_view()),

    # comment
    path('api/comment/<int:question_id>/',
         views.CommentQuestion.as_view()),
    path('api/comment/<int:question_id>/<int:answer_id>',
         views.CommentAnswer.as_view()),
    path('api/comment/question/<int:question_id>/<int:comment_id>',
         views.CommentQuestion.as_view()),
    path(
        'api/comment/answer/<int:question_id>/<int:answer_id>/<int:comment_id>', # noqa
        views.CommentAnswer.as_view()
    ),

    # Votes
    path('api/votes/upvote/<int:question_id>/', views.Upvote.as_view()),
    path(
        'api/votes/upvote/<int:question_id>/<int:answer_id>',
        views.Upvote.as_view()
    ),
    path('api/votes/downvote/<int:question_id>/', views.Downvote.as_view()),
    path(
        'api/votes/downvote/<int:question_id>/<int:answer_id>',
        views.Downvote.as_view()
    ),
    path('api/votes/unvote/<int:question_id>/', views.Unvote.as_view()),
    path(
        'api/votes/unvote/<int:question_id>/<int:answer_id>',
        views.Unvote.as_view()
    ),
]
