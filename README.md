# 🔥 SparkMatch

<p align="center">
  <img src="https://img.icons8.com/color/200/000000/tinder--v1.png" alt="SparkMatch Logo" width="200"/>
</p>

---

## 📱 Descripción

SparkMatch es una **aplicación de citas estilo Tinder** desarrollada con **Django + Python** en el backend, **PostgreSQL** como base de datos relacional y **Bootstrap 5** como único framework de frontend. El sistema es 100% funcional, 100% responsivo y está completamente dockerizado para un despliegue instantáneo.

> Desliza perfiles, da likes, genera matches mutuos y chatea en tiempo real — todo desde una interfaz moderna, fluida y sin una sola línea de CSS propio.

---

## ✨ Características

### Funcionalidades Implementadas ✅

- ✅ **Landing Page** — Presentación atractiva con animaciones y estadísticas
- ✅ **Registro & Login** — Autenticación completa con validación de formularios
- ✅ **Perfil de usuario** — Foto de perfil, bio, edad, ciudad y preferencias
- ✅ **Swipe con drag & drop** — Desliza con mouse o táctil (móvil nativo)
- ✅ **Sistema de Likes** — Like / Pass / Super Like
- ✅ **Match mutuo** — Modal de celebración cuando hay match
- ✅ **Chat en tiempo real** — Mensajería con polling cada 3 segundos
- ✅ **Lista de Matches** — Con contador de mensajes no leídos
- ✅ **Unmatch** — Eliminar match y conversación
- ✅ **Filtros por preferencia** — Por género e interés
- ✅ **Usuarios demo** — 10 perfiles de muestra al arrancar
- ✅ **Panel de administración** — Django Admin completo
- ✅ **Responsive 100%** — Mobile-first con Bootstrap 5
- ✅ **Docker Compose** — Un solo comando para correr todo

### Próximamente 🔄

- 🌍 **Filtro por distancia** — Geolocalización con PostGIS
- 🔔 **Notificaciones push** — WebSockets con Django Channels
- 📸 **Múltiples fotos** — Galería de hasta 6 imágenes
- 💎 **SparkMatch Plus** — Funciones premium
- 📊 **Estadísticas** — Dashboard de actividad
- 🤖 **IA de recomendación** — Sugerencias inteligentes de perfiles

---

## 🛠️ Stack Tecnológico

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Backend | Python / Django | 3.11 / 4.2 |
| Base de datos | PostgreSQL | 15 (Alpine) |
| Frontend | Bootstrap 5 | 5.3.3 |
| Íconos | Bootstrap Icons | 1.11.3 |
| Formularios | django-crispy-forms | 2.3 |
| Archivos estáticos | WhiteNoise | 6.7 |
| Containerización | Docker / Docker Compose | — |
| Servidor web | Django Dev / Gunicorn-ready | — |

---

## 📁 Estructura del Proyecto

```
sparkmatch/
├── 📄 docker-compose.yml        ← Orquestación de servicios
├── 📄 Dockerfile                ← Imagen de la app Django
├── 📄 entrypoint.sh             ← Setup automático al iniciar
├── 📄 requirements.txt          ← Dependencias Python
├── 📄 .dockerignore
├── 📄 README.md
└── 📂 app/
    ├── manage.py
    ├── 📂 datingapp/            ← Configuración principal Django
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── 📂 users/                ← App de usuarios & perfiles
    │   ├── models.py            ← UserProfile
    │   ├── views.py             ← Registro, login, perfil
    │   ├── forms.py             ← Formularios
    │   ├── urls.py
    │   └── management/
    │       └── commands/
    │           └── seed_demo.py ← Usuarios demo
    ├── 📂 dating/               ← App de citas
    │   ├── models.py            ← Like, Match, Message
    │   ├── views.py             ← Swipe, chat, matches
    │   ├── urls.py
    │   └── context_processors.py
    └── 📂 templates/
        ├── base.html            ← Navbar + layout global
        ├── landing.html         ← Página principal
        ├── 📂 users/
        │   ├── register.html
        │   ├── login.html
        │   ├── profile_edit.html
        │   └── profile_view.html
        └── 📂 dating/
            ├── discover.html    ← Swipe cards (Tinder UI)
            ├── matches.html     ← Lista de matches
            └── chat.html        ← Ventana de chat
```

---

## 🚀 Cómo Ejecutar el Proyecto

### Prerrequisitos
- Docker Desktop instalado ([descargar aquí](https://www.docker.com/products/docker-desktop/))
- Puerto `8000` disponible

### 1. Clonar el Repositorio
```bash
git clone https://github.com/ieharo1/sparkmatch.git
cd sparkmatch
```

### 2. Levantar con Docker Compose (recomendado)
```bash
docker-compose up --build
```

Eso es todo. El sistema automáticamente:
- ✅ Levanta PostgreSQL 15
- ✅ Aplica todas las migraciones
- ✅ Crea el usuario `admin` (contraseña: `admin123`)
- ✅ Genera 10 perfiles demo listos para usar
- ✅ Inicia la app en `http://localhost:8000`

### 3. Acceder al sistema

| URL | Descripción |
|-----|-------------|
| `http://localhost:8000` | Landing page |
| `http://localhost:8000/users/register/` | Registro |
| `http://localhost:8000/users/login/` | Login |
| `http://localhost:8000/dating/discover/` | Swipe de perfiles |
| `http://localhost:8000/dating/matches/` | Lista de matches |
| `http://localhost:8000/admin/` | Panel de administración |

### 4. Detener el sistema
```bash
docker-compose down
```

### 5. Limpiar volúmenes (reset completo)
```bash
docker-compose down -v
```

---

## 👤 Usuarios de Prueba

Al iniciar, el sistema crea automáticamente los siguientes usuarios demo (contraseña: `demo1234`):

| Usuario | Nombre | Ciudad | Género |
|---------|--------|--------|--------|
| `sofia_m` | Sofía Morales | Quito | 👩 Mujer |
| `carlos_r` | Carlos Ruíz | Guayaquil | 👨 Hombre |
| `ana_lopez` | Ana López | Cuenca | 👩 Mujer |
| `pablo_v` | Pablo Vega | Loja | 👨 Hombre |
| `valeria_c` | Valeria Castro | Ambato | 👩 Mujer |
| `miguel_t` | Miguel Torres | Riobamba | 👨 Hombre |
| `lucia_p` | Lucía Paredes | Ibarra | 👩 Mujer |
| `andres_s` | Andrés Silva | Esmeraldas | 👨 Hombre |
| `isabella_f` | Isabella Flores | Quito | 👩 Mujer |
| `diego_m` | Diego Medina | Quito | 👨 Hombre |

También existe el superusuario:
- **Usuario:** `admin` | **Contraseña:** `admin123`

---

## 🎮 Cómo Usar SparkMatch

1. **Regístrate** o usa un usuario demo
2. **Completa tu perfil** — Bio, foto, ciudad y fecha de nacimiento
3. Ve a **Descubrir** — Verás perfiles uno por uno
4. **Desliza** (drag & drop) o usa los botones:
   - ❌ **Botón rojo** — Pasar (no me interesa)
   - ⭐ **Botón azul** — Super Like
   - ❤️ **Botón rosa** — Like (me gusta)
5. Si la otra persona también te dio **Like → ¡ES UN MATCH!** 🎉
6. Ve a **Matches** para ver tus conexiones y chatear

---

## 🧱 Arquitectura del Sistema

```
┌─────────────────────────────────────────────┐
│              Docker Compose                  │
│                                             │
│   ┌─────────────────┐  ┌─────────────────┐  │
│   │   web (Django)  │  │   db (Postgres) │  │
│   │   Port: 8000    │◄─►   Port: 5432    │  │
│   │                 │  │                 │  │
│   │  ┌───────────┐  │  │   sparkmatch DB │  │
│   │  │  users    │  │  │   user: spark   │  │
│   │  │  dating   │  │  │                 │  │
│   │  └───────────┘  │  └─────────────────┘  │
│   └─────────────────┘                       │
│         │                                   │
│   ┌─────▼────────┐                          │
│   │ media/ vol.  │  ← Fotos de perfil        │
│   └──────────────┘                          │
└─────────────────────────────────────────────┘
```

---

## 📊 Modelos de Base de Datos

```
UserProfile       Like              Match             Message
──────────       ──────────        ──────────        ──────────
user (FK)        from_user (FK)    user1 (FK)        match (FK)
bio              to_user (FK)      user2 (FK)        sender (FK)
birth_date       liked (bool)      created_at        content
gender           created_at                          created_at
interested_in                                        read (bool)
location
photo
```

---

## 👨‍💻 Desarrollado por Isaac Esteban Haro Torres

**Ingeniero en Sistemas · Full Stack Developer · Automatización · Data**

### 📞 Contacto

- 📧 **Email:** zackharo1@gmail.com
- 📱 **WhatsApp:** [+593 988055517](https://wa.me/593988055517)
- 💻 **GitHub:** [ieharo1](https://github.com/ieharo1)
- 🌐 **Portafolio:** [ieharo1.github.io](https://ieharo1.github.io/portafolio-isaac.haro/)

---

## 📄 Licencia

© 2026 Isaac Esteban Haro Torres - Todos los derechos reservados.

---

⭐ Si te gustó el proyecto, ¡dame una estrella en GitHub!
