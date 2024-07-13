from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('detail/<int:post_id>/',views.PostDetailView.as_view(),name='detail'),
    path('delete/<int:post_id>/',views.PostDeleteView.as_view(),name='delete'),
    path('update/<int:post_id>/',views.PostUpdateView.as_view(),name='update'),
    path('create/',views.PostCreateView.as_view(),name='create'),
    path('reply/comment/<int:comment_id>/<int:post_id>/',views.ReplyCommentView.as_view(),name='reply'),
    path('like/<int:post_id>/',views.PostLikeView.as_view(),name='like'),
]