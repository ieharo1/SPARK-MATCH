#!/bin/bash
set -e

echo "⏳ Esperando a PostgreSQL en $POSTGRES_HOST:$POSTGRES_PORT..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 0.3
done
echo "✅ PostgreSQL listo."

echo "🔄 Aplicando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "👤 Creando superuser admin (si no existe)..."
python manage.py shell << 'PYEOF'
import datetime
from django.contrib.auth import get_user_model
from users.models import UserProfile

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser('admin', 'admin@sparkmatch.com', 'admin123')
    u.first_name = 'Admin'
    u.last_name = 'SparkMatch'
    u.save()
    UserProfile.objects.get_or_create(user=u, defaults={
        'bio': 'Administrador del sistema SparkMatch.',
        'birth_date': datetime.date(1990, 1, 1),
        'gender': 'M',
        'interested_in': 'B',
        'location': 'Quito, Ecuador'
    })
    print('Superuser admin creado (usuario: admin | pass: admin123)')
else:
    print('El superuser admin ya existe.')
PYEOF

echo "🌱 Creando usuarios demo..."
python manage.py seed_demo

echo ""
echo "SparkMatch listo en http://localhost:8000"
echo "Admin panel: http://localhost:8000/admin/"
echo "usuario: admin | contrasena: admin123"
echo ""

exec "$@"
