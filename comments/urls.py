from django.conf.urls import url

from . import views

app_name = 'comment'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^listComments/$', views.list_comments, name='list_comments'),
    url(r'^voteComment/$', views.vote, name='vote_comment'),
]