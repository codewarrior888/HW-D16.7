from django.urls import path
from .views import CommentApproval, CommentsList, PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, MyPostList

urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='post_search'),
    path('search/<int:pk>', PostDetail.as_view(), name='post_detail_search'),
    path('posts/create/', PostCreate.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('accounts/profile/', MyPostList.as_view(), name='profile'),
    path('myposts/', MyPostList.as_view(), name='mypost_list'),
    path('myposts/<int:pk>', PostDetail.as_view(), name='mypost_detail'),
    path('usercomments/', CommentsList.as_view(), name='usercomments'),
    path('comment_approval/', CommentApproval.as_view(), name='comment_approval'),
]
