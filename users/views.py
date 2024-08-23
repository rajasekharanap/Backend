from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from.serializers import UserSignupSerializer, UserLoginSerializer, PostSerializer
from .models import Post

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user)
            post_serializer = PostSerializer(post)
            return Response({'data': post_serializer.data, 'message': 'Post is created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublishPostView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, author= request.user)
        except Post.DoesNotExist:
            return Response({"message": "Post not found or you are not the author of this post."}, status=status.HTTP_404_NOT_FOUND)
        post.published = True
        post.save()
        post_serializer = PostSerializer(post)
        return Response({'data': post_serializer.data, 'message': 'Post published successfully'}, status=status.HTTP_200_OK)
        
class UnpublishPostView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id, author=request.user)
        except Post.DoesNotExist:
            return Response({"message": "Post not found or you are not the author of this post."}, status=status.HTTP_404_NOT_FOUND)

        post.published = False
        post.save()

        post_serializer = PostSerializer(post)
        return Response({'data': post_serializer.data, 'message': 'Post unpublished successfully'}, status=status.HTTP_200_OK)