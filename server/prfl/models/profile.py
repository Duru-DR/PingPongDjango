from django.db                  import models
from authentication.models      import CustomUser
from django.core.exceptions     import ValidationError
from django.utils.translation   import gettext_lazy as _

# def validate_image(file):
#     file_size = file.size
#     limit_kb = 1024 * 7  # 7 MB limit
#     if file_size > limit_kb * 1024:
#         raise ValidationError("Max file size is %s KB" % limit_kb)
#     if not file.content_type.startswith('image/'):
#         raise ValidationError("Only image files are allowed")
    
class Profile(models.Model):
    BADGE_CHOICES = [
        ('BRONZE', 'Bronze'),
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum'),
        ('DIAMOND', 'Diamond'),
        ('HEROIC', 'Heroic'),
        ('GRAND_MASTER', 'Grand Master'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    email = models.CharField(_("email"), max_length=150, unique=True, blank=True)
    username = models.CharField(_("username"), max_length=150, unique=True, blank=True)
    first_name = models.CharField(_("first_name"), max_length=150, blank=True, null=True)
    last_name = models.CharField(_("last_name"), max_length=150, blank=True, null=True)
    is_online = models.BooleanField(_("is_online"), default=False)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    picture = models.CharField(_("pic"), max_length=150, blank=True, null=True)
    background_picture = models.CharField(_("back pic"), max_length=150, blank=True, null=True)
    # picture = models.ImageField(blank=True, null=True)
    # background_picture = models.ImageField(blank=True, null=True)
    rank = models.IntegerField(_("Rank"), default=0)
    wins = models.IntegerField(_("wins"), default=0)
    loses = models.IntegerField(_("loses"), default=0)
    isSettings = models.BooleanField(_("isSettings"), default=False)
    isInviting = models.BooleanField(_("isInviting"), default=False)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    badge = models.CharField(
        max_length=15,
        choices=BADGE_CHOICES,
        default='BRONZE',
    )
    
    play_requests = models.ManyToManyField('self', symmetrical=False, related_name='received_play_requests', blank=True)

    def __str__(self):
        return self.username
