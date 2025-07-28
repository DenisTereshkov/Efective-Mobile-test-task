from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .constants import (
    CATEGORY_CHOICES,
    CONDITION_CHOICES,
    STATUS_CHOICES
)
from .models import Ad, ExchangeProposal
from .forms import AdForm

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('ads_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = AdForm()
    
    return render(request, 'ads/ad_create_edit.html', {'form': form})

@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads_list')
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_create_edit.html', {'form': form})


def ads_list(request):
    ads = Ad.objects.exclude(received_proposals__status='accepted').order_by('-created_at')
    search_query = request.GET.get('search', '')
    if search_query:
        ads = ads.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    category = request.GET.get('category')
    if category:
        ads = ads.filter(category=category)
    condition = request.GET.get('condition')
    if condition:
        ads = ads.filter(condition=condition)
    paginator = Paginator(ads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    my_ads = request.user.ads.all() if request.user.is_authenticated else []
    context = {
        'page_obj': page_obj,
        'categories': CATEGORY_CHOICES,
        'conditions': CONDITION_CHOICES,
        'search_query': search_query,
        'selected_category': category or '',
        'selected_condition': condition or '',
        'my_ads': my_ads
    }
    return render(request, 'ads/ads_list.html', context)


@login_required
def create_exchange(request, pk):  # Используем pk как в других views
    receiver_ad = get_object_or_404(Ad, id=pk)
    if request.user == receiver_ad.user:
        messages.error(request, "Вы не можете предлагать обмен на своё же объявление!")
        return redirect('detail', pk=pk)
    
    if request.method == 'POST':
        sender_ad_id = request.POST.get('sender_ad_id')
        comment = request.POST.get('comment', '')
        
        try:
            sender_ad = Ad.objects.get(id=sender_ad_id, user=request.user)
            ExchangeProposal.objects.create(
                ad_sender=sender_ad,
                ad_receiver=receiver_ad,
                comment=comment,
                status='pending'
            )
            messages.success(request, 'Предложение отправлено!')
            return redirect('detail', pk=pk)
        except Exception as e:
            messages.error(request, f'Ошибка: {e}')
            return redirect('create_exchange', pk=pk)
    
    # GET-запрос: показываем форму
    user_ads = Ad.objects.filter(user=request.user).exclude(id=pk)
    return render(request, 'ads/create_exchange.html', {
        'receiver_ad': receiver_ad,
        'user_ads': user_ads,
    })



def ad_detail(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    return render(request, 'ads/ad_detail.html', {'ad': ad})

@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.user != ad.user:
        messages.error(request, 'Вы не можете удалить это объявление')
        return redirect('ads_list')
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Объявление успешно удалено')
        return redirect('profile')
    return render(request, 'ads/confirm_delete.html', {'ad': ad})


@login_required
def user_profile(request):
    user_ads = Ad.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ads/profile.html', {'ads': user_ads})

def incoming_exchanges(request):
    proposals = ExchangeProposal.objects.filter(
        ad_receiver__user=request.user
    )
    return render(request, 'ads/exchange_to_me.html', {'proposals': proposals})

def accept_exchange(request, exchange_id):
    proposal = get_object_or_404(ExchangeProposal, id=exchange_id)
    proposal.status = 'accepted'
    proposal.save()
    return redirect('exchange_to_me')

def reject_exchange(request, exchange_id):
    proposal = get_object_or_404(ExchangeProposal, id=exchange_id)
    proposal.status = 'rejected'
    proposal.save()
    return redirect('exchange_to_me')