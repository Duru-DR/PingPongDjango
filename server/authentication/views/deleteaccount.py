from rest_framework import generics, status
from ..utils import Authenticate, gen_token, print_green, print_red
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from prfl.models import Profile
from django.core.mail       import send_mail
from django.core.mail       import EmailMessage
from django.template.loader import render_to_string

User = get_user_model()

class DeleteAccountView(generics.GenericAPIView):
    def get(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        email = user.email
        token = gen_token(user)
        reset_url = f'http://10.12.1.4/settings?token={token}'
        subject = 'Deleting PingPong Account'
        message = render_to_string('emaildelete.html', {
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
            {"message": "Email sent successfully."},
            status=status.HTTP_200_OK
        )
