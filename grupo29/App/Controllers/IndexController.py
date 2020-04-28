from django.shortcuts import render,HttpResponse
class IndexController():
    def index(request):
        #return HttpResponse('<h5> ppp </h5>')
        return render(request,'views/index/index.html')