from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('armytrg/', views.armytrg, name='armytrg'),
    path('crevent/', views.create_event, name='crevent'),
    path('crparticipant/', views.create_participant, name='crparticipant'),
    path('participantevent/', views.participant_event, name='participantevent'),
    path('participantview/', views.participant_view, name='participantview'),
    path('crcourseoffer/', views.creat_course_offer, name='crcourseoffer'),
    path('cwisecourseoffer/', views.coffer_by_country, name='cwisecourseoffer'),
    path('codbysvc/', views.codby_services, name='codbysvc'),
    path('crofficersandstaffs/', views.crofficersandstaffs, name='crofficersandstaffs'),
    path('disofficersandstaffs/', views.disofficersandstaffs, name='disofficersandstaffs'),
    path('creventforcal/', views.create_event, name='creventforcal'),
    path('disevent/', views.event_list, name='disevent'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)