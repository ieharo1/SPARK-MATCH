from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q
from django.contrib import messages
from .models import Like, Match, Message
from users.models import UserProfile


def get_or_create_match(user1, user2):
    """Retorna el match ordenando por id para evitar duplicados."""
    if user1.id < user2.id:
        u1, u2 = user1, user2
    else:
        u1, u2 = user2, user1
    match, created = Match.objects.get_or_create(user1=u1, user2=u2)
    return match, created


@login_required
def discover(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    # Usuarios ya valorados
    already_seen = Like.objects.filter(from_user=request.user).values_list('to_user_id', flat=True)
    
    # Filtrar por preferencias
    q = UserProfile.objects.exclude(user=request.user).exclude(user_id__in=already_seen)
    
    if profile.interested_in == 'M':
        q = q.filter(gender='M')
    elif profile.interested_in == 'F':
        q = q.filter(gender='F')
    
    # Excluir perfiles sin fecha de nacimiento para mostrar solo perfiles completos
    q = q.filter(birth_date__isnull=False).select_related('user').order_by('?')
    
    candidates = list(q[:20])
    current_profile = candidates[0] if candidates else None
    remaining = len(candidates) - 1

    return render(request, 'dating/discover.html', {
        'profile': profile,
        'current_profile': current_profile,
        'remaining': remaining,
    })


@login_required
def swipe(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    to_user_id = request.POST.get('to_user_id')
    action = request.POST.get('action')  # 'like' or 'pass'
    
    if not to_user_id or action not in ('like', 'pass'):
        return JsonResponse({'error': 'Datos inválidos'}, status=400)
    
    to_user = get_object_or_404(User, id=to_user_id)
    liked = action == 'like'
    
    Like.objects.get_or_create(
        from_user=request.user,
        to_user=to_user,
        defaults={'liked': liked}
    )
    
    is_match = False
    match_id = None
    match_name = None
    match_photo = None
    
    if liked:
        # Verificar si hay like mutuo
        mutual = Like.objects.filter(from_user=to_user, to_user=request.user, liked=True).exists()
        if mutual:
            match, created = get_or_create_match(request.user, to_user)
            if created:
                is_match = True
                match_id = match.id
                match_name = to_user.get_full_name() or to_user.username
                other_profile = UserProfile.objects.filter(user=to_user).first()
                match_photo = other_profile.get_photo_url() if other_profile else ''
    
    return JsonResponse({
        'success': True,
        'is_match': is_match,
        'match_id': match_id,
        'match_name': match_name,
        'match_photo': match_photo,
    })


@login_required
def matches_list(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    
    user_matches = Match.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).select_related('user1', 'user2').order_by('-created_at')
    
    matches_data = []
    for match in user_matches:
        other = match.get_other_user(request.user)
        other_profile = UserProfile.objects.filter(user=other).first()
        last_msg = match.get_last_message()
        unread = match.unread_count(request.user)
        matches_data.append({
            'match': match,
            'other_user': other,
            'other_profile': other_profile,
            'last_message': last_msg,
            'unread': unread,
        })
    
    return render(request, 'dating/matches.html', {
        'matches_data': matches_data,
        'profile': profile,
    })


@login_required
def chat(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    
    if request.user not in [match.user1, match.user2]:
        messages.error(request, 'No tienes acceso a este chat.')
        return redirect('matches_list')
    
    other_user = match.get_other_user(request.user)
    other_profile = UserProfile.objects.filter(user=other_user).first()
    
    # Marcar mensajes como leídos
    match.messages.filter(read=False).exclude(sender=request.user).update(read=True)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content and len(content) <= 1000:
            Message.objects.create(
                match=match,
                sender=request.user,
                content=content
            )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
        return redirect('chat', match_id=match_id)
    
    chat_messages = match.messages.select_related('sender').all()
    my_profile = UserProfile.objects.filter(user=request.user).first()
    
    return render(request, 'dating/chat.html', {
        'match': match,
        'other_user': other_user,
        'other_profile': other_profile,
        'chat_messages': chat_messages,
        'my_profile': my_profile,
    })


@login_required
def get_new_messages(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.user not in [match.user1, match.user2]:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    last_id = request.GET.get('last_id', 0)
    new_msgs = match.messages.filter(id__gt=last_id).select_related('sender')
    new_msgs.filter(read=False).exclude(sender=request.user).update(read=True)
    
    data = []
    for msg in new_msgs:
        my_profile = UserProfile.objects.filter(user=msg.sender).first()
        data.append({
            'id': msg.id,
            'sender_id': msg.sender.id,
            'sender_name': msg.sender.get_full_name() or msg.sender.username,
            'sender_photo': my_profile.get_photo_url() if my_profile else '',
            'content': msg.content,
            'created_at': msg.created_at.strftime('%H:%M'),
            'is_mine': msg.sender == request.user,
        })
    return JsonResponse({'messages': data})


@login_required
def unmatch(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.user in [match.user1, match.user2]:
        other = match.get_other_user(request.user)
        match.delete()
        Like.objects.filter(
            Q(from_user=request.user, to_user=other) |
            Q(from_user=other, to_user=request.user)
        ).delete()
        messages.success(request, 'Has eliminado este match.')
    return redirect('matches_list')
