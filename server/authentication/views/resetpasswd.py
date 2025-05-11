from rest_framework         import generics, status
from django.http            import JsonResponse
from django.conf            import settings
from django.contrib.auth    import get_user_model
from ..utils                import decodeJWTToken

User = get_user_model()

class ResetPasswd(generics.GenericAPIView):
    def post(self, request, token):
        password1 = request.data['password1']
        password2 = request.data['password2']

        if (not password1 or not password2) or (password1 != password2):
            return JsonResponse(
                {"message": "Unmatched Passswords"},
                status = status.HTTP_400_BAD_REQUEST
            )
        tk = decodeJWTToken(token)
        if not tk:
            return JsonResponse(
                {"message": "Invalid Request"},
                status = status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.get(id=tk['user_id'])
        user.set_password(password1)
        user.save()
        return JsonResponse(
            {"message": "Password has been reset successfully"},
            status = status.HTTP_200_OK
        )