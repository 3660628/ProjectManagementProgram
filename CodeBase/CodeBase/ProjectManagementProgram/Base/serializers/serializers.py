# Python Imports
import datetime

# Django Imports
from rest_framework import serializers
from django.contrib.auth.models import User
from Base.models import UserExtra
from Base.models import Project
from Base.models import UserProject
from Base.models import Link
from Base.models import Alert
from Base.models import File
from Base.models import Discussion
from Base.models import Comment
from Base.models import Blog
from Base.models import BlogPost


class UserSerializer(serializers.ModelSerializer):
    """
    UserSerializer which overrides create and update methods.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        user_object = User(username=validated_data['username'])
        user_object.set_password(validated_data['password'])
        if 'email' in validated_data:
            user_object.email = validated_data['email']
        if 'first_name' in validated_data:
            user_object.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            user_object.last_name = validated_data['last_name']
        user_object.save()
        return user_object

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        if 'email' in validated_data:
            instance.email = validated_data['email']
        if 'first_name' in validated_data:
            instance.first_name = validated_data['first_name']
        if 'last_name' in validated_data:
            instance.last_name = validated_data['last_name']
        instance.save()
        return instance


class UserExtraSerializer(serializers.ModelSerializer):
    """
    UserExtraSerializer
    """
    class Meta:
        model = UserExtra
        fields = ('id', 'user', 'company', 'department', 'description')
        read_only_fields = ('id',)


generic_fields = [
    'id',
    'user_creator',
    'date_created',
    'user_last_modified',
    'last_modified',
    'user_closed',
    'date_closed',
    'is_active']


class ProjectSerializer(serializers.ModelSerializer):
    """
    ProjectSerializer which overrides the create method.
    """
    class Meta:
        model = Project
        fields = ('id', 'title', 'homepage_text', 'conclusion', 'is_active')
        read_only_fields = ('id', 'is_active')

    def create(self, validated_data):
        project_object = super(ProjectSerializer, self).create(validated_data)
        request = self.context.get('request', None)
        user_object = User.objects.get(username=request.user.username)
        user_project_object = UserProject(user=user_object,
                                          project=project_object,
                                          is_creator=True)
        user_project_object.save()
        return project_object


class UserProjectSerializer(serializers.ModelSerializer):
    """
    UserProjectSerializer.
    """
    class Meta:
        model = UserProject
        fields = ('id', 'user', 'project', 'is_creator', 'is_admin', 'is_active')
        read_only_fields = ('id', 'is_active')


class LinkSerializer(serializers.ModelSerializer):
    """
    LinkSerializer which overrides the create and update methods.
    """
    class Meta:
        model = Link
        fields = tuple(generic_fields + ['project', 'title', 'link_text', 'description'])
        read_only_fields = tuple(generic_fields)

    def create(self, validated_data):
        request = self.context.get('request', None)
        user_object = User.objects.get(username=str(request.user.username))
        returned_object = Link(user_creator=user_object,
                               project=validated_data['project'],
                               title=validated_data['title'],
                               link_text=validated_data['link_text'])
        if 'description' in validated_data:
            returned_object.description = validated_data['description']
        returned_object.save()
        return returned_object

    def update(self, instance, validated_data):
        returned_object = super(LinkSerializer, self).update(instance, validated_data)
        request = self.context.get('request', None)
        user_object = User.objects.get(username=request.user.username)
        returned_object.user_last_modified = user_object
        returned_object.last_modified = datetime.date.today()
        returned_object.save()
        return returned_object


class AlertSerializer(serializers.ModelSerializer):
    """
    AlertSerializer.
    """
    class Meta:
        model = Alert
        fields = ('id', 'project', 'alert', 'user_creator', 'date_created')
        read_only_fields = ('id',)


class FileSerializer(serializers.ModelSerializer):
    """
    FileSerializer which overrides the create and update methods.
    """
    class Meta:
        model = File
        fields = tuple(generic_fields + ['project', 'title', 'description', 'file'])
        read_only_fields = tuple(generic_fields)

    def create(self, validated_data):
        request = self.context.get('request', None)
        user_object = User.objects.get(username=str(request.user.username))
        returned_object = File(user_creator=user_object,
                               project=validated_data['project'],
                               title=validated_data['title'])
        if 'description' in validated_data:
            returned_object.description = validated_data['description']
        if 'file' in validated_data:
            returned_object.description = validated_data['file']
        returned_object.save()
        return returned_object

    def update(self, instance, validated_data):
        returned_object = super(FileSerializer, self).update(instance, validated_data)
        request = self.context.get('request', None)
        user_object = User.objects.get(username=request.user.username)
        returned_object.user_last_modified = user_object
        returned_object.last_modified = datetime.date.today()
        returned_object.save()
        return returned_object


class DiscussionSerializer(serializers.ModelSerializer):
    """
    DiscussionSerializer which overrides the create and update methods.
    """
    class Meta:
        model = Discussion
        fields = tuple(generic_fields + ['project', 'title', 'description', 'conclusion'])
        read_only_fields = tuple(generic_fields)

    def create(self, validated_data):
        request = self.context.get('request', None)
        user_object = User.objects.get(username=str(request.user.username))
        returned_object = Discussion(user_creator=user_object,
                                     project=validated_data['project'],
                                     title=validated_data['title'])
        if 'description' in validated_data:
            returned_object.description = validated_data['description']
        returned_object.save()
        return returned_object

    def update(self, instance, validated_data):
        returned_object = super(DiscussionSerializer, self).update(instance, validated_data)
        request = self.context.get('request', None)
        user_object = User.objects.get(username=request.user.username)
        returned_object.user_last_modified = user_object
        returned_object.last_modified = datetime.date.today()
        returned_object.save()
        return returned_object


class CommentSerializer(serializers.ModelSerializer):
    """
    CommentSerializer which overrides the create and update methods.
    """
    class Meta:
        model = Comment
        fields = tuple(generic_fields + ['project', 'discussion', 'comment_text'])
        read_only_fields = tuple(generic_fields)

    def create(self, validated_data):
        request = self.context.get('request', None)
        user_object = User.objects.get(username=str(request.user.username))
        returned_object = Comment(user_creator=user_object,
                                  project=validated_data['project'],
                                  discussion=validated_data['discussion'],
                                  comment_text=validated_data['comment_text'])
        returned_object.save()
        return returned_object

    def update(self, instance, validated_data):
        returned_object = super(CommentSerializer, self).update(instance, validated_data)
        request = self.context.get('request', None)
        user_object = User.objects.get(username=request.user.username)
        returned_object.user_last_modified = user_object
        returned_object.last_modified = datetime.date.today()
        returned_object.save()
        return returned_object


class BlogSerializer(serializers.ModelSerializer):
    """
    BlogSerializer which overrides the create and update methods.
    """
    class Meta:
        model = Blog
        fields = tuple(generic_fields + ['project', 'title', 'description'])
        read_only_fields = tuple(generic_fields)

    def create(self, validated_data):
        request = self.context.get('request', None)
        user_object = User.objects.get(username=str(request.user.username))
        returned_object = Blog(user_creator=user_object,
                               project=validated_data['project'],
                               title=validated_data['title'])
        if 'description' in validated_data:
            returned_object.description = validated_data['description']
        returned_object.save()
        return returned_object

    def update(self, instance, validated_data):
        returned_object = super(BlogSerializer, self).update(instance, validated_data)
        request = self.context.get('request', None)
        user_object = User.objects.get(username=request.user.username)
        returned_object.user_last_modified = user_object
        returned_object.last_modified = datetime.date.today()
        returned_object.save()
        return returned_object


class BlogPostSerializer(serializers.ModelSerializer):
    """
    BlogPostSerializer which overrides the create and update methods.
    """
    class Meta:
        model = BlogPost
        fields = tuple(generic_fields + ['blog', 'parent_entry', 'post', 'project'])
        read_only_fields = tuple(generic_fields)

    def create(self, validated_data):
        request = self.context.get('request', None)
        user_object = User.objects.get(username=str(request.user.username))
        returned_object = BlogPost(user_creator=user_object,
                                   blog=validated_data['blog'],
                                   project=validated_data['project'],
                                   post=validated_data['post'])
        if 'parent_entry' in validated_data:
            returned_object.parent_entry = validated_data['parent_entry']
        returned_object.save()
        return returned_object

    def update(self, instance, validated_data):
        returned_object = super(BlogPostSerializer, self).update(instance, validated_data)
        request = self.context.get('request', None)
        user_object = User.objects.get(username=request.user.username)
        returned_object.user_last_modified = user_object
        returned_object.last_modified = datetime.date.today()
        returned_object.save()
        return returned_object
