import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import UserProfile


DEMO_USERS = [
    {'username': 'sofia_m', 'first': 'Sofía', 'last': 'Morales', 'gender': 'F', 'interested_in': 'M', 'age_offset': -24, 'location': 'Quito, Ecuador', 'bio': '📸 Fotógrafa de corazón. Amo los viajes, el café y los atardeceres desde el Telefériko ✈️☕'},
    {'username': 'carlos_r', 'first': 'Carlos', 'last': 'Ruíz', 'gender': 'M', 'interested_in': 'F', 'age_offset': -27, 'location': 'Guayaquil, Ecuador', 'bio': '🎸 Músico y foodie. Toco en una banda de rock. ¿Te gusta el sushi? 🍣'},
    {'username': 'ana_lopez', 'first': 'Ana', 'last': 'López', 'gender': 'F', 'interested_in': 'B', 'age_offset': -22, 'location': 'Cuenca, Ecuador', 'bio': '👩‍⚕️ Estudiante de medicina. Fan de los libros, el yoga y los perros 🐶📚'},
    {'username': 'pablo_v', 'first': 'Pablo', 'last': 'Vega', 'gender': 'M', 'interested_in': 'F', 'age_offset': -29, 'location': 'Loja, Ecuador', 'bio': '💻 Dev & gamer. Busco a alguien que aprecie los memes y las pizzas a las 2am 🍕'},
    {'username': 'valeria_c', 'first': 'Valeria', 'last': 'Castro', 'gender': 'F', 'interested_in': 'M', 'age_offset': -25, 'location': 'Ambato, Ecuador', 'bio': '🌺 Diseñadora gráfica. Pintura acuarela, plantas y cine independiente 🎨🌿'},
    {'username': 'miguel_t', 'first': 'Miguel', 'last': 'Torres', 'gender': 'M', 'interested_in': 'F', 'age_offset': -31, 'location': 'Riobamba, Ecuador', 'bio': '🏔️ Alpinista. He escalado el Chimborazo 3 veces. El frío no me asusta 🏕️'},
    {'username': 'lucia_p', 'first': 'Lucía', 'last': 'Paredes', 'gender': 'F', 'interested_in': 'M', 'age_offset': -23, 'location': 'Ibarra, Ecuador', 'bio': '🎭 Actriz de teatro amateur. Me río de todo y bailo en la cocina 🎶💃'},
    {'username': 'andres_s', 'first': 'Andrés', 'last': 'Silva', 'gender': 'M', 'interested_in': 'F', 'age_offset': -26, 'location': 'Esmeraldas, Ecuador', 'bio': '🏄 Surfer y chef improvisado. Si cocino para ti, es porque me gustas 🍳'},
    {'username': 'isabella_f', 'first': 'Isabella', 'last': 'Flores', 'gender': 'F', 'interested_in': 'M', 'age_offset': -21, 'location': 'Quito, Ecuador', 'bio': '🌸 Emprendedora. Tengo una tienda de ropa vintage. Vintage vibes only 👗✨'},
    {'username': 'diego_m', 'first': 'Diego', 'last': 'Medina', 'gender': 'M', 'interested_in': 'B', 'age_offset': -28, 'location': 'Quito, Ecuador', 'bio': '🎬 Director de cortometrajes. La vida es más interesante en 24 fps 🎞️'},
]


class Command(BaseCommand):
    help = 'Crea usuarios demo para SparkMatch'

    def handle(self, *args, **kwargs):
        today = datetime.date.today()
        created = 0
        for u in DEMO_USERS:
            if User.objects.filter(username=u['username']).exists():
                continue
            user = User.objects.create_user(
                username=u['username'],
                password='demo1234',
                first_name=u['first'],
                last_name=u['last'],
                email=f"{u['username']}@sparkmatch.demo"
            )
            bday = today.replace(year=today.year + u['age_offset'])
            UserProfile.objects.create(
                user=user,
                gender=u['gender'],
                interested_in=u['interested_in'],
                birth_date=bday,
                location=u['location'],
                bio=u['bio'],
            )
            created += 1
            self.stdout.write(self.style.SUCCESS(f'  ✅ Creado: {user.get_full_name()} (@{user.username})'))
        self.stdout.write(self.style.SUCCESS(f'\n🎉 {created} usuarios demo creados. Contraseña: demo1234'))
