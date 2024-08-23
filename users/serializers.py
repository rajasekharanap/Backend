from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Tag, Post
import re


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'mobile', 'username', 'password']

    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Please enter a valid email address.")
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def validate_mobile(self, value):
        phone_regex = r'^\+91[6-9][0-9]{9}$'
        if not re.match(phone_regex, value):
            raise serializers.ValidationError("Please enter a valid phone number.")
        return value

    def validate_password(self, value):
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password should contain at least one letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password should contain at least one digit.")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'],
            mobile=validated_data['mobile'],
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid Credentials")
        return {
            'user': user,
            'username': data['username'],
            'password': data['password']
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id','title', 'description', 'tags', 'created_at', 'published']
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            post.tags.add(tag)
        return post

