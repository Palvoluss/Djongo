import profile
from django.shortcuts import render, redirect, get_object_or_404
from app.models import Wallet
from app.utils import generate_random_number
from .forms import UserSignInForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def register(request):

    context = { }

    if request.method == "POST":
        form = UserSignInForm(request.POST)
        if form.is_valid():

            user = form.save()
            token_balance = generate_random_number(10)
            wallet = Wallet.objects.create(
                user = user, token_balance = token_balance
            )
            wallet.save()
            messages.success(request, f"Your account has been created! You are now able to log in and start trade your token")
            return redirect('login')
            
    else: 
        form = UserSignInForm()
      
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)




# def user_detail(request, pk):
#     user = get_object_or_404(User, pk=pk)

#     context = {
#         'user': user, 
#     }
#     return render(request, 'users/user_detail.html', context)