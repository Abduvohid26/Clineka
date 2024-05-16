import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from .utils import phone_regex
import random
from rest_framework_simplejwt.tokens import RefreshToken
ADMIN, DOCTOR, ORDINARY_USER = ('admin', 'doctor', 'ordinary_user')


class User(AbstractUser):
    USER_ROLES = (
        (ADMIN, ADMIN),
        (DOCTOR, DOCTOR),
        (ORDINARY_USER, ORDINARY_USER),
    )
    REGION = (
        ('Toshkent', 'Toshkent'),
        ("Farg'ona", "Farg'ona"),
        ("Andijon", "Andijon"),
        ("Namangan", "Namangan"),
        ("Qoraqolpag'iston", "Qoraqolpag'iston"),
        ("Samarqand", "Samarqand"),
        ("Qashqadaryo", "Qashqadaryo"),
        ("Surxondaryo", "Surxondaryo"),
        ("Xorazim", "Xorazim"),
        ("Sirdaryo", "Sirdaryo"),
        ("Jizzah", "Jizzah"),
        ("Navoiy", "Navoiy"),
        ("Buxoro", "Buxoro")

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_roles = models.CharField(max_length=100, choices=USER_ROLES, default=ORDINARY_USER)
    phone_number = models.CharField(max_length=13, validators=[phone_regex], unique=True)
    region = models.CharField(max_length=255, choices=REGION)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username

    def token(self):
        refresh = RefreshToken.for_user(self)
        access_token = refresh.access_token
        # Add custom claims to the access token
        access_token['user_roles'] = self.user_roles
        access_token['exp'] = int(access_token['exp'])
        return {
            'access_token': str(access_token),
            'refresh_token': str(refresh),
        }

    def check_hash_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def check_username(self):
        if not self.username:
            temp_username = f'cashcare1234-{uuid.uuid4().__str__().split("-")[-1]}'
            while User.objects.filter(username=temp_username):
                temp_username = f'{temp_username}{random.randint(0, 9)}'
            self.username = temp_username

    def save(self, *args, **kwargs):
        self.check_hash_password()
        self.check_username()
        super(User, self).save(*args, **kwargs)


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_patient')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.sender} {self.doctor}'



