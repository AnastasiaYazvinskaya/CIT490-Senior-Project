from django.shortcuts import render, redirect
from trainer.models import PrepareUser

# Home page
def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'index.html')

def table(request):
    objects = PrepareUser.objects.all().order_by('active')
    
    return render(request, 'table.html', {'objects': objects})