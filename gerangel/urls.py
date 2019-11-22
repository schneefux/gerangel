from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from matchlog import views as matchlog_views
from matchmake import views as matchmake_views

router = routers.DefaultRouter()
router.register(r'users', matchlog_views.UserViewSet, 'user')
router.register(r'players', matchlog_views.PlayerViewSet, 'player')
router.register(r'matches', matchlog_views.MatchViewSet, 'matches')
router.register(r'match-results', matchlog_views.MatchResultViewSet, 'matches-results')
router.register(r'match-players', matchlog_views.MatchPlayerViewSet, 'match-players')
router.register(r'matchmake', matchmake_views.MatchmakeViewSet, 'matchmake')

urlpatterns = [
    path('', include(router.urls)),
    # TODO logout & delete/expire tokens, see djoser or django-rest-auth
    path('login', obtain_auth_token, name='login'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
