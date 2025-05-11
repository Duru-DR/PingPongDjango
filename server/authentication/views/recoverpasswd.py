from rest_framework         import generics, status
from django.http            import JsonResponse
from django.contrib.auth    import get_user_model
from django.conf            import settings
from django.core.mail       import send_mail
from django.core.mail       import EmailMessage
from django.template.loader import render_to_string
from ..utils                import gen_token

User = get_user_model()

class RequestReset(generics.GenericAPIView):
    def post(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first()

        if not email:
            return JsonResponse(
                {"message": "Email is required"},
                status = status.HTTP_400_BAD_REQUEST
            )
        if user:
            token = gen_token(user)
            reset_url = f'http://localhost:8080/resetpassword/{token}'
            subject = 'Password Reset Request'
            message = render_to_string('emailreset.html', {
                'user': user,
                'reset_url': reset_url,
            })
            email = EmailMessage(
                subject=subject,
                body=message,
                from_email='teamfttranscendence@gmail.com',
                to=[email],
            )
            email.content_subtype = 'html'
            email.send()
            return JsonResponse(
                {"message": "Password reset email sent"},
                status = status.HTTP_200_OK
            )
        return JsonResponse(
            {"message": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    