from django.urls import path
from .views import UserLoginView, UserSignupView, PostCreateView


urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('createpost/', PostCreateView.as_view(), name='create_post'),

]