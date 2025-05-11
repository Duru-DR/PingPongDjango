from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenView.as_view(), name='token'),
    path('GnrToken/', GnrToken.as_view(), name='GenerateTokens'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('intra42/callback/', IntraOAuthView.as_view(), name='OAuhtIntra'),
    path('google/callback/', GoogleOAuthView.as_view(), name='OAuthGoogle'),
    path('passwd/verify/', VerifyPasswd.as_view(), name='Passwdverify'),
    path('2fa/enable/', Enable2fa.as_view(), name='enable2fa'),
    path('2fa/disable/', Disable2fa.as_view(), name='disable2fa'),
    path('2fa/verify/device/', VerifyDevice.as_view(), name='VerrifyDevice'),
    path('2fa/verify/', Verify2fa.as_view(), name='verify2fa'),
    path('2fa/backup-codes/', GenerateBackupCodes.as_view(), name='Backup-codes'),
    path('passwordrecovery/', RequestReset.as_view(), name='Request reset password'),
    path('passwordreset/<str:token>/', ResetPasswd.as_view(), name='Password reset'),
    path('passwordchange/', ChangePasswd.as_view(), name='Password change'),
    path('deleteaccount/', DeleteAccountView.as_view()),
    path('deleteaccount/check/<str:token>/', DeleteAccountAffected.as_view()),
]
