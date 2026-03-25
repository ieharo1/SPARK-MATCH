from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='Sobre mí')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Fecha de nacimiento')),
                ('gender', models.CharField(choices=[('M', 'Hombre'), ('F', 'Mujer'), ('O', 'Otro')], default='O', max_length=1, verbose_name='Género')),
                ('interested_in', models.CharField(choices=[('M', 'Hombres'), ('F', 'Mujeres'), ('B', 'Todos')], default='B', max_length=1, verbose_name='Me interesan')),
                ('location', models.CharField(blank=True, max_length=100, verbose_name='Ciudad')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profiles/', verbose_name='Foto de perfil')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
    ]
