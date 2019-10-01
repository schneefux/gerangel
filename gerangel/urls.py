from django.urls import include, path
from rest_framework import routers
from matchlog import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'user')
router.register(r'players', views.PlayerViewSet, 'player')
router.register(r'matches', views.MatchViewSet, 'matches')
router.register(r'match-results', views.MatchResultViewSet, 'matches-results')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
