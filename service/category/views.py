from django.shortcuts import render
from django.http import( HttpRequest,HttpResponse,HttpResponseRedirect,Http404)
from django.template import loader


# Create your views here.
def home(request):
    return render(request,'blog-details.html')