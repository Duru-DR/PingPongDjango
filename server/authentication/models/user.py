from django.apps                                    import apps
from django.db                                      import models
from django.contrib.auth.models                     import AbstractUser, UserManager
from django.utils.translation                       import gettext_lazy as _
from authentication.models.utils.validate_email     import validate_email
from authentication.models.utils.validate_passwd    import validate_password
from authentication.models.utils.validate_name      import validate_name
from authentication.models.utils.validate_username  import validate_username
from django.core.exceptions                         import ValidationError

class CustomUserManager(UserManager):
    
    def create_user(self, username, email, password, **extra_fields):

        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not password:
            raise ValueError("The given password must be set")
        if not email:
            raise ValueError("The given email must be set")
        
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError({"password": str(e)})
    
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label,
            self.model._meta.object_name,
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
    
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
   
    first_name = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        validators=[validate_name]
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        validators=[validate_name]
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[validate_email]
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        validators=[validate_username]
    )
    
    last_login = models.DateTimeField(_("last login"), auto_now=True)
    token_last_change = models.DateTimeField(null=True, blank=True)
    is_2fa_enabled = models.BooleanField(_("is_2fa_enabled"), default=False)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.username
