from django.shortcuts import render, redirect

# Home page
def index(request):
    #if request.user.is_authenticated:
    #    return redirect('home')
    #else:
    return render(request, 'index.html')