from rest_framework             import generics, status
from django.http                import JsonResponse
from authentication.utils       import Authenticate

class EditAddressView(generics.GenericAPIView):
    def post(self, request):
        user = Authenticate(request)
        if not user.is_authenticated:
            return JsonResponse(
                {"message": "User is not authenticated"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        country = request.data.get('country')
        city = request.data.get('city')
        address = request.data.get('address')
        zip_code = request.data.get('Code')
        profile = user.profile
        if country:
            profile.country = country
            profile.save()
        if city:
            profile.city = city
            profile.save()
        if address:
            profile.address = address
            profile.save()
        if zip_code:
            profile.zip_code = zip_code
            profile.save()
        return JsonResponse(
            {"message": "Address data updated successfully"},
            status = status.HTTP_200_OK
        )
