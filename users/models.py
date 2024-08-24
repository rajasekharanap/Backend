from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
class CustomUser(AbstractBaseUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    username = models.CharField(max_length=255, unique=True)

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    

class Post(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return f"{self.title} created by {self.author}"

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.name} likes the post {self.post.title}"
