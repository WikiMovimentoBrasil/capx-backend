from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .forms import ProfileForm
# TODO pensar nas telas básicas
# TODO criar alguns dados no BD para ter dados para puxar para resultados na tela


def homepage(request):
    context = {}
    return render(request, "users/index.html", context)


@login_required()
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to view profile after successful edit
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'users/profile.html', {'form': form})


def login_oauth(request):
    return redirect(reverse('social:begin', kwargs={"backend": "mediawiki"}))


def logout(request):
    auth_logout(request)
    return redirect(reverse('homepage'))
