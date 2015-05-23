from rest_framework import permissions
from Base.models import UserProject
from django.contrib.auth.models import User


class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of their own user object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj == request.user


class IsUserExtraOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of their own user extra object to edit it.
    """
    def has_permission(self, request, view):

        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        user_to_create_user_extra_object_for = User.objects.get(id=request.POST['user']).id
        return user_to_create_user_extra_object_for == request.user.id


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.user_creator == request.user


class IsOwnerOrProjectMembersReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Only project members can view.
    """
    def has_object_permission(self, request, view, obj):
        # Get user project object.
        if UserProject.objects.filter(user=request.user, project__id=obj.project.id, is_active=True).exists():
            # Read permissions are allowed to any request, so we'll always allow GET, HEAD or OPTIONS requests.
            if request.method in permissions.SAFE_METHODS:
                return True

            # Write permissions are only allowed to the owner of the object.
            return obj.user_creator == request.user

        # Return False as user is not a project member.
        else:
            return False


class IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly2(permissions.BasePermission):
    """
    Custom permission to only allow project owners or admins and to edit the project.
    Only project members can view project objects.
    """
    def has_object_permission(self, request, view, obj):
        # Get user project object.
        if UserProject.objects.filter(user=request.user, project__id=obj.id, is_active=True).exists():
            user_project_object = UserProject.objects.get(user__username=request.user.username,
                                                          project__id=obj.id,
                                                          is_active=True)

            # Read permissions are allowed to any project member, so we'll always allow GET, HEAD or OPTIONS requests.
            if request.method in permissions.SAFE_METHODS:
                return True

            # Allow if user is a project owner/creator.
            if user_project_object.is_creator:
                return True

            # Allow if user is a project admin.
            if user_project_object.is_admin:
                return True

        # Return False as user is not a project member.
        else:
            return False


class IsProjectOwnerOrProjectAdminOrProjectMembersReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow project owners or admins and to edit project objects.
    Only project members can view project objects.
    """
    def has_object_permission(self, request, view, obj):

        # Get user project object.
        if UserProject.objects.filter(user=request.user, project__id=obj.project.id, is_active=True).exists():
            user_project_object = UserProject.objects.get(user=request.user,
                                                          project__id=obj.project.id,
                                                          is_active=True)

            # Read permissions are allowed to any project member, so we'll always allow GET, HEAD or OPTIONS requests.
            if request.method in permissions.SAFE_METHODS:
                return True

            # Allow if user is a project owner/creator.
            elif user_project_object.is_creator:
                return True

            # Allow if user is a project admin.
            elif user_project_object.is_admin:
                return True

            else:
                return False

        # Return False as user is not a project member.
        else:
            return False


class IsProjectMemberOnly(permissions.BasePermission):
    """
    Custom permission to allow project members to perform actions.
    """
    def has_permission(self, request, view):
        if UserProject.objects.filter(user=request.user,
                                      project__id=request.POST['project'],
                                      is_active=True).exists():
            return True
        else:
            return False


class IsProjectAdminOrProjectCreator(permissions.BasePermission):
    """
    Custom permission to allow only project admins or project creator to perform an action.
    """
    def has_permission(self, request, view):
        if UserProject.objects.filter(user=request.user,
                                      project__id=request.POST['project'],
                                      is_active=True,
                                      is_admin=True).exists():
            return True
        elif UserProject.objects.filter(user=request.user,
                                        project__id=request.POST['project'],
                                        is_active=True,
                                        is_creator=True).exists():
            return True
        else:
            return False
