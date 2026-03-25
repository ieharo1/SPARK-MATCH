from django.db.models import Q
from .models import Match


def unread_messages_count(request):
    if request.user.is_authenticated:
        matches = Match.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        )
        count = 0
        for match in matches:
            count += match.unread_count(request.user)
        return {'unread_messages_total': count}
    return {'unread_messages_total': 0}
