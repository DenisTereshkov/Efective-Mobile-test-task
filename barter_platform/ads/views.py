from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Ad
from .forms import AdForm

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            return redirect('ads_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_create.html', {'form': form})

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
    return render(request, 'ads/ad_form.html', {'form': form})

def ads_list(request):
    ads = Ad.objects.all().order_by('-created_at')
    return render(request, 'ads/ads_list.html', {'ads': ads})

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
