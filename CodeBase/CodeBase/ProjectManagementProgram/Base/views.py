from Base.serializers.serializers import UserSerializer
from Base.serializers.serializers import UserExtraSerializer
from Base.serializers.serializers import ProjectSerializer
from Base.serializers.serializers import UserProjectSerializer
from Base.serializers.serializers import LinkSerializer
from Base.serializers.serializers import AlertSerializer
from Base.serializers.serializers import FileSerializer
from Base.serializers.serializers import DiscussionSerializer
from Base.serializers.serializers import CommentSerializer
from Base.serializers.serializers import BlogSerializer
from Base.serializers.serializers import BlogPostSerializer
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
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from Base.permissions.permissions import IsUserOrReadOnly
from Base.permissions.permissions import IsUserExtraOrReadOnly
from Base.permissions.permissions import IsOwnerOrReadOnly
from Base.permissions.permissions import IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly
from Base.permissions.permissions import IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly2
from Base.permissions.permissions import IsProjectMemberOnly
from Base.permissions.permissions import IsOwnerOrProjectMembersReadOnly
from Base.permissions.permissions import IsProjectAdminOrProjectCreator


class UserList(generics.ListCreateAPIView):
    """
    Anyone can list all Users, or create a new User.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    If authenticated a user can retrieve, update or delete their own User instance.
    """
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserExtraList(generics.ListCreateAPIView):
    """
    If authenticated a user can list all UserExtras, or create a new UserExtra.
    """
    permission_classes = (IsAuthenticated, IsUserExtraOrReadOnly)
    queryset = UserExtra.objects.all()
    serializer_class = UserExtraSerializer


class UserExtraDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    If authenticated a user can retrieve, update or delete their UserExtra instance.
    """
    permission_classes = (IsAuthenticated, IsUserExtraOrReadOnly)
    queryset = UserExtra.objects.all()
    serializer_class = UserExtraSerializer


class ProjectList(generics.ListCreateAPIView):
    """
    If authenticated a user can list all Projects, or create a Project.
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    If a project member a user can retrieve a Project instance,
    If project owner or Project admin a user can update or delete a Project instance.
    """
    permission_classes = (IsAuthenticated, IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly2)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class UserProjectList(generics.ListCreateAPIView):
    """
    If a project member a user can retrieve a UserProject instance,
    If project owner or Project admin a user can update or delete a UserProject instance.

    Using this class a user can:
    Add a user to the project.
    Remove a user from a project.
    Make user a project admin.
    Make user a standard project member.
    """
    permission_classes = (IsAuthenticated, IsProjectAdminOrProjectCreator)
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer


class UserProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    If a project member a user can retrieve UserProject instances.
    If object owner a user can update or delete a UserProject instance.

    Using this class a user can:
    Add themselves toa project.
    Remove themselves from a project.
    """
    permission_classes = (IsAuthenticated, IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly)
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer


class LinkList(generics.ListCreateAPIView):
    """
    Project members can list all Links, or create a new Link.
    """
    permission_classes = (IsAuthenticated, IsProjectMemberOnly)
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Project members can retrieve a Link instance.
    Project owner and project admins can update or delete a Link instance.
    """
    permission_classes = (IsAuthenticated, IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly)
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class AlertList(generics.ListCreateAPIView):
    """
    Project members can list all Alerts, or create a new Alert.
    """
    permission_classes = (IsAuthenticated, IsProjectMemberOnly)
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


class AlertDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Project members can retrieve an Alert instance.
    Project owner and project admins can update or delete an Alert instance.
    """
    permission_classes = (IsAuthenticated, IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly)
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


class FileList(generics.ListCreateAPIView):
    """
    Project members can list all Files, or create a new File.
    """
    permission_classes = (IsAuthenticated, IsProjectMemberOnly)
    queryset = File.objects.all()
    serializer_class = FileSerializer


class FileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Project members can retrieve a File instance.
    Project owner and project admins can update or delete a File instance.
    """
    permission_classes = (IsAuthenticated, IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly)
    queryset = File.objects.all()
    serializer_class = FileSerializer


class DiscussionList(generics.ListCreateAPIView):
    """
    Project members can list all Discussions, or create a new Discussion.
    """
    permission_classes = (IsAuthenticated, IsProjectMemberOnly)
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer


class DiscussionDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Project members can retrieve a Discussion instance.
    Project owner and project admins can update or delete a Discussion instance.
    """
    permission_classes = (IsAuthenticated, IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly)
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer


class CommentList(generics.ListCreateAPIView):
    """
    Project members can list all Comments, or create a new Comment.
    """
    permission_classes = (IsAuthenticated, IsProjectMemberOnly)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Project members can retrieve a Comment instance.
    Object owner and project admins can update or delete a Comment instance.
    """
    permission_classes = (IsAuthenticated, IsOwnerOrProjectMembersReadOnly)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class BlogList(generics.ListCreateAPIView):
    """
    Project members can list all Blogs, or create a new Blog.
    """
    permission_classes = (IsAuthenticated, IsProjectMemberOnly)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Project members can retrieve a Blog instance.
    Project owner and project admins can update or delete a Blog instance.
    """
    permission_classes = (IsAuthenticated, IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly)
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogPostList(generics.ListCreateAPIView):
    """
    Project members can list all BlogPosts, or create a new BlogPost.
    """
    permission_classes = (IsAuthenticated, IsProjectMemberOnly)
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class BlogPostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Project members can retrieve a BlogPost instance.
    Object owner and project admins can update or delete a BlogPost instance.
    """
    permission_classes = (IsAuthenticated, IsOwnerOrProjectMembersReadOnly)
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
