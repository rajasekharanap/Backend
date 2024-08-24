from django.urls import path
from .views import UserLoginView, UserSignupView, PostCreateView, PublishPostView, UnpublishPostView, PostsListview, PostLikeUnlikeView, TagSearchView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
    path('publish_post/<int:post_id>/', PublishPostView.as_view(), name='publish_post'),
    path('unpublish_post/<int:post_id>/', UnpublishPostView.as_view(), name='publish_post'),
    path('published_posts/',PostsListview.as_view(), name='published_posts'),
    path('like_unlike_posts/<int:post_id>/', PostLikeUnlikeView.as_view(), name='post_like_unlike'),
    path('search_tag/', TagSearchView.as_view(), name='tag_search'),

]