from django.shortcuts import render

# Create your views here.


def server(request):
    return render(request, 'MyServer/server.html')
