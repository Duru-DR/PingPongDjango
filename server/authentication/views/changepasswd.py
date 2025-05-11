from rest_framework import generics, status
from django.http    import JsonResponse
from datetime       import datetime, timezone
from ..utils        import Authenticate, JWTsGenerator

class ChangePasswd(generics.GenericAPIView):
    def post(self, request):
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        if not old_password or not new_password:
            return JsonResponse(
                {"message": "Old password and new password are required"},
                status = status.HTTP_400_BAD_REQUEST
            )

        if user.check_password(old_password):
            user.set_password(new_password)
            user.token_last_change = datetime.now(timezone.utc) 
            user.save()
            return JWTsGenerator(
                user.id,
                {"message": "Your password has been changed successfully. You have been logged out of all active sessions."}
            )
        return JsonResponse(
            {"message": "Incorrect old password"},
            status = status.HTTP_400_BAD_REQUEST
        )
