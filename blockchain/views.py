from django.contrib.auth.decorators import login_required
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse

from .models import Wallet


@login_required
def create_wallet(request):
    if request.user.is_authenticated:
        data = request.POST
        if data['passphrase'] == data['passphrase2']:
            wallet, created = Wallet.objects.update_or_create(
                user=request.user)
            wallet.create_account(data['passphrase2'])

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(wallet).pk,
                object_id=wallet.id,
                object_repr=str(wallet),
                action_flag=ADDITION,
                change_message='Created wallet for %s' % wallet.user)

        return redirect(reverse('dashboard:wallet'))

    else:
        return redirect(reverse('dashboard:dashboard'))
