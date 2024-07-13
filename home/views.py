from django.shortcuts import render
from django.views import View
from posts.models import Post
from .forms import SearchForm


class HomePageView(View):
    form_class = SearchForm

    def get(self,request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        return render(request,'home/home.html',{'posts':posts,'form':self.form_class})