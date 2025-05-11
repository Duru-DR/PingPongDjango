from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

urlpatterns = [
    path('data/', ProfileDataView.as_view()),
    path('data/<str:username>/', UserProfileView.as_view()),
    path('statistics/', StatisticsView.as_view()),
    path('friends/', FriendsListView.as_view()),
    path('blocked-friends/', BlockedFriendsView.as_view()),
    path('requested-friendships/', RequestedFriendshipsView.as_view()),
    path('friendship-requests/', FriendshipsRequestsView.as_view()),
    path('search/', SearchProfilesView.as_view()),
    path('search/friends/', SearchFriendsView.as_view()),
    path('notifications/', Notifications.as_view()),
    path('personal-data/', PersonalDataView.as_view()),
    path('customize-pics/', CustomizePicsView.as_view()),
    path('edit/personal-data/', EditPersonalDataView.as_view()),
    path('edit/address/', EditAddressView.as_view()),
    path('block-friend/', BlockFriendView.as_view()),
    path('unblock-friend/', UnBlockFriendView.as_view()),
    path('send-friendship-request/', SendFriendshipRequestView.as_view()),
    path('handle-friendship-request/', HandleFriendshipRequestView.as_view()),
    path('eliminate-friendship-request/', EliminateFriendshipRequestView.as_view()),
    path('send-palywithme-request/', SendPlayWithMeRequestView.as_view()),
    path('notification/join-tournament/', SendJoinTournamentNotificationView.as_view()),
    path('notification/tournament-reminder/', TournamentReminderNotificationView.as_view()),
    path('user/', UserProfileView.as_view()),
    path('WhoAmI/', WhoAmI.as_view()),
    path('upload-picture/', ProfileImageUploadView.as_view()),
    path('upload-background_picture/', ProfileBackgroundUploadView.as_view()),
]
