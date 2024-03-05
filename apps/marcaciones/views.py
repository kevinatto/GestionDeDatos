from django.shortcuts import render

# Create your views here.
def proceso(request):
    return render(request, 'marcaciones/proceso.html')