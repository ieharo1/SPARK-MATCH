from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Hombre'),
        ('F', 'Mujer'),
        ('O', 'Otro'),
    ]
    INTEREST_CHOICES = [
        ('M', 'Hombres'),
        ('F', 'Mujeres'),
        ('B', 'Todos'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Sobre mí')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O', verbose_name='Género')
    interested_in = models.CharField(max_length=1, choices=INTEREST_CHOICES, default='B', verbose_name='Me interesan')
    location = models.CharField(max_length=100, blank=True, verbose_name='Ciudad')
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name='Foto de perfil')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_age(self):
        if self.birth_date:
            today = timezone.now().date()
            age = today.year - self.birth_date.year
            if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
                age -= 1
            return age
        return None

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return f"https://ui-avatars.com/api/?name={self.user.first_name}+{self.user.last_name}&size=400&background=e91e63&color=fff&bold=true&rounded=true"

    def is_complete(self):
        return bool(self.bio and self.birth_date and self.location)

    def __str__(self):
        return f"Perfil de {self.user.get_full_name() or self.user.username}"
