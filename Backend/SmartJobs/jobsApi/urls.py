from django.urls import  path
from . import views


urlpatterns = [
    path('ap/',views.jobsAP.as_view(),name='jobsAP'),
    path('the/',views.jobsTHE.as_view(),name='jobsTHE'),
    path('up/',views.jobsUP.as_view(),name='jobsUP'),
    path('like/',views.likeJob.as_view(),name='likeJob'),
    path('labels/',views.labels.as_view(),name='labels'),
    path('jobs/',views.jobs.as_view(),name='jobs'),
    path('query/',views.query.as_view(),name='query'),
    path('inbox/',views.inbox.as_view(),name='inbox'),
    path('signup/',views.signup.as_view(),name='signup'),
    path('signin/',views.signin.as_view(),name='signin'),
    path('shquery/',views.searchhistoryquery.as_view(),name='searchhistoryquery'),
    path('shresult/', views.getsearchhistory.as_view(), name='getsearchhistory'),
    path('scheduled/',views.startScheduled,name="scheduled"),
    path('',views.index,name='index'),

]
