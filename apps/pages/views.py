from django.shortcuts import render

def index(request):
    return render(request, 'pages/index.html')

def about_view(request):
    return render(request, "pages/about.html")
