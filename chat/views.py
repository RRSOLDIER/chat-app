from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.shortcuts import render,redirect

from django.contrib.auth import get_user_model
from .models import Message
User = get_user_model()


@login_required
def user_listview(request):
    users=User.objects.exclude(id=request.user.id)
    return render(request,'user_list.html',{'users':users})

@login_required
def chat_view(request, user_id):

    other_user = get_object_or_404(User, id=user_id)

    room_name = get_room_name(request.user, other_user)

    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return render(request, 'chat.html', {
        'receiver': other_user,
        'room_name': room_name,
        'messages': messages,
    })

def get_room_name(user1, user2):
    users = sorted([str(user1.id), str(user2.id)])
    return f"{users[0]}_{users[1]}"
