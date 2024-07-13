from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from .models import Post,Comment,Vote
from django.contrib import messages
from .forms import PostCreateUpdateForm,CommentForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin


class PostDetailView(View):
    form_class = CommentForm

    def setup(self,request,*args,**kwargs):
        self.post_instance = get_object_or_404(Post,id=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        post = self.post_instance
        comments = post.comments.filter(is_reply=False)
        can_like = True
        if request.user.is_authenticated and self.post_instance.can_like(request.user):
            can_like = False
        return render(request,'posts/detail.html',{'post':post,'comments':comments,
                                                   'form':self.form_class,'can_like':can_like})
    
    def post(self,request,*args,**kwargs):
        post = self.post_instance
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request,'Your comment sent','success')
            return redirect('posts:detail',post.id)
    
class PostDeleteView(LoginRequiredMixin,View):

    def setup(self,request,*args,**kwargs):
        self.post_instance = get_object_or_404(Post,id=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)
    
    def dispatch(self,request,*args,**kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request,'This post is not for you','danger')
            return redirect('posts:detail',post.id)
        return super().dispatch(request,*args,**kwargs)
    
    def get(self,request,post_id):
        post = self.post_instance
        post.delete()
        messages.success(request,'The post deleted','success')
        return redirect('home:home')

class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm

    def setup(self,request,*args,**kwargs):
        self.post_instance = get_object_or_404(Post,id=kwargs['post_id'])
        return super().setup(request,*args,**kwargs)
    
    def dispatch(self,request,*args,**kwargs):
        post = self.post_instance
        if not request.user.id == post.user.id:
            messages.error(request,'The post is not for you','danger')
            return redirect('posts:detail',self.post_instance.id)            
        return super().dispatch(request,*args,**kwargs)
        
    def get(self,request,post_id):
        form = self.form_class(instance=self.post_instance)
        return render(request,'posts/update.html',{'form':form})
    
    def post(self,request,post_id):
        post = self.post_instance
        form = self.form_class(request.POST,instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:20])
            new_post.save()
            messages.success(request,'The post updated','success')
            return redirect('posts:detail',post.id)
        
class PostCreateView(LoginRequiredMixin,View):
    form_class = PostCreateUpdateForm


    def get(self,request):
        form = self.form_class
        return render(request,'posts/create.html',{'form':form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.slug = slugify(form.cleaned_data['body'][:20])
            new_post.save()
            messages.success(request,'You have successfully a post created','success')
            return redirect('accounts:profile',request.user.id)
        
class ReplyCommentView(View):

    def post(self,request,comment_id,post_id):
        comment = get_object_or_404(Comment,id=comment_id)
        post = get_object_or_404(Post,id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            new_reply = form.save(commit=False)
            new_reply.user = request.user
            new_reply.post = post
            new_reply.reply = comment
            new_reply.is_reply = True
            new_reply.save()
            messages.success(request,'Your comment sent','success')
            return redirect('posts:detail',post.id)

class PostLikeView(View):

    def get(self,request,post_id):
        post = get_object_or_404(Post,id=post_id)
        vote = Vote.objects.filter(user=request.user,post=post).exists()
        if vote:
            messages.error(request,'You liked already this post','danger')
        else:
            Vote.objects.create(user=request.user,post=post)
            messages.success(request,'Liked','success')
        return redirect('posts:detail',post.id)

