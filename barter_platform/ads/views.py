from django.shortcuts import render, redirect, get_object_or_404
from .models import Ad
from .forms import AdForm

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
    return render(request, 'ads/ad_form.html', {'form': form})

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
    return render(request, 'ads_list.html', {'ads': ads})