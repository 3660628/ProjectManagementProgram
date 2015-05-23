# Django Imports
from django.test import TestCase
from django.test import Client
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


class GenericTestCase(TestCase):
    """
    Boilerplate for other tests. This sets up a project and adds the following users/members and permissions:
    username = roy, project creator
    username = paul, project admin
    username = harry, project member
    username = james, user but not member of the project
    """
    def setUp(self):
        self.client = Client()
        # Create users and test.
        self.new_user_data = [{'username': 'roy', 'password': 'password1'},
                              {'username': 'paul', 'password': 'password2'},
                              {'username': 'harry', 'password': 'password3'},
                              {'username': 'james', 'password': 'password4'}]
        self.__create_users__()
        for new_user in self.new_user_data:
            self.assertEqual(User.objects.filter(username=new_user['username']).exists(), True)
        self.__log_users_in__()

        # Create user 'roy' project to become project creator and test.
        self.roy_client.post('/api/project/',
                             {'title': 'My First Project',
                              'homepage_text': 'Welcome to My First Project'})
        self.project_id = Project.objects.get(title='My First Project', homepage_text='Welcome to My First Project').id
        self.assertEqual(Project.objects.filter(title='My First Project',
                                                homepage_text='Welcome to My First Project').exists(), True)
        self.assertEqual(Project.objects.filter(title='My First Project',
                                                homepage_text='Welcome to My First Project').count() == 1, True)
        self.assertEqual(Project.objects.filter(title='My First Project',
                                                homepage_text='Welcome to My First Project').exists(), True)
        self.assertEqual(UserProject.objects.filter(user__username='roy',
                                                    project__title='My First Project',
                                                    is_creator=True).exists(), True)
        self.assertEqual(UserProject.objects.filter(user__username='roy',
                                                    project__title='My First Project',
                                                    is_creator=True).count() == 1, True)
        # Adding two other users.
        self.roy_client.post('/api/user_project/',
                             {'user': User.objects.get(username='paul').id,
                              'project': Project.objects.get(title='My First Project').id,
                              'is_admin': 'True'})
        self.assertEqual(UserProject.objects.filter(user__username='paul',
                                                    project__title='My First Project',
                                                    is_admin=True).exists(), True)
        self.assertEqual(UserProject.objects.filter(user__username='paul',
                                                    project__title='My First Project',
                                                    is_admin=True).count() == 1, True)
        self.roy_client.post('/api/user_project/',
                             {'user': User.objects.get(username='harry').id,
                              'project': Project.objects.get(title='My First Project').id})
        self.assertEqual(UserProject.objects.filter(user__username='harry',
                                                    project__title='My First Project',
                                                    is_admin=False).exists(), True)
        self.assertEqual(UserProject.objects.filter(user__username='harry',
                                                    project__title='My First Project',
                                                    is_admin=False).count() == 1, True)
        self.assertEqual(UserProject.objects.filter(user__username='James',
                                                    project__title='My First Project').exists(), False)

    def __create_users__(self):
        """
        Creates test users.
        """
        for new_user in self.new_user_data:
            self.client.post('/api/user/', new_user)

    def __log_users_in__(self):
        """
        Log users created in.
        """
        self.roy_client = Client()
        self.roy_client.login(username='roy', password='password1')
        self.paul_client = Client()
        self.paul_client.login(username='paul', password='password2')
        self.harry_client = Client()
        self.harry_client.login(username='harry', password='password3')
        self.james_client = Client()
        self.james_client.login(username='james', password='password4')

########################################################################################################################
# UserExtra
########################################################################################################################


class UserExtraTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()
        self.__test_four__()

    def __test_one__(self):
        """
        User creates their own user extra object.
        """
        self.roy_client.post('/api/user_extra/', {'user': str(User.objects.get(username='roy').id),
                                                  'company': 'abc company',
                                                  'department': 'abc department',
                                                  'description': 'abc description'})
        self.assertEqual(UserExtra.objects.filter(user__username='roy',
                                                  company='abc company',
                                                  department='abc department',
                                                  description='abc description').exists(), True)

    def __test_two__(self):
        """
        User tries to edit their own user extra object.
        """
        object_id = UserExtra.objects.get(user__username='roy',
                                          company='abc company',
                                          department='abc department',
                                          description='abc description').id
        self.roy_client.post('/api/user_extra/%s/' % str(object_id), {'_method': 'PUT',
                                                                      'user': User.objects.get(username='roy').id,
                                                                      'company': '123 company',
                                                                      'department': '123 department',
                                                                      'description': '123 description'})
        self.assertEqual(UserExtra.objects.filter(user__username='roy',
                                                  company='abc company',
                                                  department='abc department',
                                                  description='abc description').exists(), False)
        self.assertEqual(UserExtra.objects.filter(user__username='roy',
                                                  company='123 company',
                                                  department='123 department',
                                                  description='123 description').exists(), True)
        self.assertEqual(UserExtra.objects.filter(user__username='roy').count() == 1, True)

    def __test_three__(self):
        """
        User tries to edit another users user extra object. This will fail.
        """
        self.paul_client.post('/api/user_extra/', {'user': str(User.objects.get(username='paul').id),
                                                   'company': 'paul company',
                                                   'department': 'paul department',
                                                   'description': 'paul description'})
        object_id = UserExtra.objects.get(user__username='roy').id
        self.roy_client.post('/api/user_extra/%s/' % str(object_id), {'id': object_id,
                                                                      'user': User.objects.get(username='paul').id,
                                                                      'company': 'abc company',
                                                                      'department': 'abc department',
                                                                      'description': 'abc description'})
        self.assertEqual(UserExtra.objects.filter(user__username='paul',
                                                  company='abc company',
                                                  department='abc department',
                                                  description='abc description').exists(), False)
        self.assertEqual(UserExtra.objects.filter(user__username='paul',
                                                  company='paul company',
                                                  department='paul department',
                                                  description='paul description').exists(), True)

    def __test_four__(self):
        """
        User creates user extra object for another user. This will fail.
        """
        self.roy_client.post('/api/user_extra/', {'user': str(User.objects.get(username='harry').id),
                                                  'company': 'abc company',
                                                  'department': 'abc department',
                                                  'description': 'abc description'})
        self.assertEqual(UserExtra.objects.filter(user__username='harry',
                                                  company='abc company',
                                                  department='abc department',
                                                  description='abc description').exists(), False)

########################################################################################################################
# Project
########################################################################################################################


class ProjectTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()

    def __test_one__(self):
        """
        User creates a project. along with the user project instance.
        """
        self.roy_client.post('/api/project/', {'title': 'test project 2', 'homepage_text': 'welcome to my project'})
        self.assertEqual(Project.objects.filter(title='test project 2',
                                                homepage_text='welcome to my project').exists(), True)
        self.assertEqual(UserProject.objects.filter(user__id=User.objects.get(username='roy').id,
                                                    project__id=Project.objects.get(title='test project 2').id,
                                                    is_creator=True,
                                                    is_admin=False,
                                                    is_active=True).exists(), True)

    def __test_two__(self):
        """
        Users will try to edit the home page of a project. Only project creators and admins can do this.
        """
        self.roy_client.post('/api/project/%s/' % str(self.project_id), {'_method': 'PUT',
                                                                         'title': 'test project 3',
                                                                         'homepage_text': 'welcome to you all!!'})
        self.assertEqual(Project.objects.filter(id=str(self.project_id),
                                                title='test project 3',
                                                homepage_text='welcome to you all!!').exists(), True)
        self.paul_client.post('/api/project/%s/' % str(self.project_id), {'_method': 'PUT',
                                                                          'title': 'test project 4',
                                                                          'homepage_text': 'welcome!'})
        self.assertEqual(Project.objects.filter(id=str(self.project_id),
                                                title='test project 4',
                                                homepage_text='welcome!').exists(), True)
        self.harry_client.post('/api/project/%s/' % str(self.project_id), {'_method': 'PUT',
                                                                           'title': 'test project 5',
                                                                           'homepage_text': 'welcome'})
        self.assertEqual(Project.objects.filter(id=str(self.project_id),
                                                title='test project 5',
                                                homepage_text='welcome').exists(), False)
        self.assertEqual(Project.objects.filter(id=str(self.project_id),
                                                title='test project 4',
                                                homepage_text='welcome!').exists(), True)

    def __test_three__(self):
        """
        User will delete/close the project. Only the project creator can do this.
        """
        self.assertEqual(UserProject.objects.filter(user__id=str(User.objects.get(username='paul').id),
                                                    project__id=str(self.project_id)).exists(), True)
        self.paul_client.post('/api/project/%s/' % str(self.project_id), {'_method': 'DELETE',
                                                                          'conclusion': 'paul close'})
        self.assertEqual(Project.objects.filter(id=str(self.project_id),
                                                conclusion='paul close',
                                                is_active=False).exists(), False)
        self.assertEqual(UserProject.objects.filter(user__id=str(User.objects.get(username='roy').id),
                                                    project__id=str(self.project_id)).exists(), True)
        self.roy_client.post('/api/project/%s/' % str(self.project_id), {'_method': 'DELETE',
                                                                         'conclusion': 'roy close'})
        self.assertEqual(Project.objects.filter(id=str(self.project_id),
                                                is_active=False).exists(), True)

########################################################################################################################
# UserProject
########################################################################################################################


class UserProjectTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()
        self.__test_four__()

    def __test_one__(self):
        """
        Creator will add and remove a non project member to a project.
        """
        non_project_member_id = User.objects.get(username='james').id

        self.roy_client.post('/api/user_project/',
                             {'user': non_project_member_id,
                              'project': self.project_id})
        self.assertEqual(UserProject.objects.filter(user__id=str(non_project_member_id),
                                                    project__id=str(self.project_id),
                                                    is_active=True).exists(), True)

        non_project_user_id = UserProject.objects.get(user__id=str(non_project_member_id),
                                                      project__id=str(self.project_id),
                                                      is_active=True).id
        self.roy_client.post('/api/user_project/%s/' % non_project_user_id, {'_method': 'DELETE'})
        self.assertEqual(UserProject.objects.filter(user__id=str(non_project_member_id),
                                                    project__id=str(self.project_id),
                                                    is_active=False).exists(), True)

        self.assertEqual(UserProject.objects.filter(user__id=str(non_project_member_id),
                                                    project__id=str(self.project_id),
                                                    is_active=True).exists(), False)

    def __test_two__(self):
        """
        Admin will add and remove a non project member to a project.
        """
        non_project_member_id = User.objects.get(username='james').id
        self.paul_client.post('/api/user_project/',
                              {'user': non_project_member_id,
                               'project': self.project_id})
        self.assertEqual(UserProject.objects.filter(user__id=str(non_project_member_id),
                                                    project__id=str(self.project_id),
                                                    is_active=True).exists(), True)
        non_project_user_id = UserProject.objects.get(user__id=str(non_project_member_id),
                                                      project__id=str(self.project_id),
                                                      is_active=True).id
        self.paul_client.post('/api/user_project/%s/' % non_project_user_id, {'_method': 'DELETE'})
        self.assertEqual(UserProject.objects.filter(user__id=str(non_project_member_id),
                                                    project__id=str(self.project_id),
                                                    is_active=False).exists(), True)
        self.assertEqual(UserProject.objects.filter(user__id=str(non_project_member_id),
                                                    project__id=str(self.project_id),
                                                    is_active=True).exists(), False)

    def __test_three__(self):
        """
        A standard will add and remove a non project member to a project. This should fail.
        """
        non_project_member_id = User.objects.get(username='james').id
        self.harry_client.post('/api/user_project/', {'user': non_project_member_id,
                                                      'project': self.project_id})

        self.assertEqual(UserProject.objects.filter(user__id=str(non_project_member_id),
                                                    project__id=str(self.project_id),
                                                    is_active=True).exists(), False)

    def __test_four__(self):
        """
        A standard will change the a project admin to a standard user. This should fail.
        """
        admin_project_member_id = UserProject.objects.get(user__username='paul', project__id=self.project_id).id
        self.james_client.post('/api/user_project/%s/' % str(admin_project_member_id), {'_method': 'PUT',
                                                                                        'is_admin': False})

        self.assertEqual(UserProject.objects.filter(user__id=str(admin_project_member_id),
                                                    project__id=str(self.project_id),
                                                    is_admin=True).exists(), True)

########################################################################################################################
# Link
########################################################################################################################


class LinkTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()
        self.__test_four__()
        self.__test_five__()
        self.__test_six__()

    def __test_one__(self):
        """
        Non project member adds a link. This should fail.
        """
        self.james_client.post('/api/link/', {'project': self.project_id,
                                              'title': 'james new link',
                                              'link_text': 'www.google.com'})
        self.assertEqual(Link.objects.filter(user_creator__id=str(User.objects.get(username='james').id),
                                             project__id=str(self.project_id)).exists(), False)

    def __test_two__(self):
        """
        Project member adds a link.
        """
        self.paul_client.post('/api/link/', {'project': self.project_id,
                                             'title': 'paul new link',
                                             'link_text': 'www.google.com'})
        self.assertEqual(Link.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new link',
                                             link_text='www.google.com',
                                             project__id=str(self.project_id)).exists(), True)

    def __test_three__(self):
        """
        Project member edits a link. This should fail.
        """
        link_object_id = Link.objects.get(project__id=self.project_id,
                                          title='paul new link',
                                          link_text='www.google.com').id
        self.harry_client.post('/api/link/%d/' % link_object_id, {'_method': 'PUT',
                                                                  'user': User.objects.get(username='paul').id,
                                                                  'project': self.project_id,
                                                                  'title': 'harry\'s new link',
                                                                  'link_text': 'www.google.com'})
        self.assertEqual(Link.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new link',
                                             link_text='www.google.com',
                                             project__id=str(self.project_id)).exists(), True)
        self.assertEqual(Link.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='harry\'s new link',
                                             link_text='www.google.com',
                                             project__id=str(self.project_id)).exists(), False)

    def __test_four__(self):
        """
        Project admin edits a link.
        """
        link_object_id = Link.objects.get(project__id=self.project_id,
                                          title='paul new link',
                                          link_text='www.google.com').id
        self.paul_client.post('/api/link/%d/' % link_object_id, {'_method': 'PUT',
                                                                 'user': User.objects.get(username='paul').id,
                                                                 'project': self.project_id,
                                                                 'title': 'test test test',
                                                                 'link_text': 'www.google.com'})
        self.assertEqual(Link.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new link',
                                             link_text='www.google.com',
                                             project__id=str(self.project_id)).exists(), False)
        self.assertEqual(Link.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='test test test',
                                             link_text='www.google.com',
                                             project__id=str(self.project_id)).exists(), True)

    def __test_five__(self):
        """
        Project member removes a link. This should fail.
        """
        link_object_id = Link.objects.get(project__id=self.project_id,
                                          title='test test test',
                                          link_text='www.google.com').id
        self.harry_client.post('/api/link/%d/' % link_object_id, {'_method': 'DELETE'})
        self.assertEqual(Link.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='test test test',
                                             link_text='www.google.com',
                                             project__id=str(self.project_id),
                                             is_active=True).exists(), True)

    def __test_six__(self):
        """
        Project admin removes a link.
        """
        link_object_id = Link.objects.get(project__id=self.project_id,
                                          title='test test test',
                                          link_text='www.google.com').id
        self.paul_client.post('/api/link/%d/' % link_object_id, {'_method': 'DELETE'})
        self.assertEqual(Link.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='test test test',
                                             link_text='www.google.com',
                                             project__id=str(self.project_id),
                                             is_active=True).exists(), False)

########################################################################################################################
# Alert
########################################################################################################################


class AlertTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()
        self.__test_four__()
        self.__test_five__()
        self.__test_six__()

    def __test_one__(self):
        """
        Non project member adds an Alert. This should fail.
        """
        self.james_client.post('/api/alert/', {'user_creator': User.objects.get(username='james').id,
                                               'project': self.project_id,
                                               'alert': 'james new alert'})
        self.assertEqual(Alert.objects.filter(user_creator__id=str(User.objects.get(username='james').id),
                                              project__id=str(self.project_id),
                                              alert='james new alert').exists(), False)

    def __test_two__(self):
        """
        Project member adds an Alert.
        """
        self.harry_client.post('/api/alert/', {'user_creator': User.objects.get(username='harry').id,
                                               'project': self.project_id,
                                               'alert': 'harry new alert'})
        self.assertEqual(Alert.objects.filter(user_creator__id=str(User.objects.get(username='harry').id),
                                              project__id=str(self.project_id),
                                              alert='harry new alert').exists(), True)

    def __test_three__(self):
        """
        Project member edits an Alert. This should fail.
        """
        alert_object_id = Alert.objects.get(project__id=self.project_id,
                                            alert='harry new alert').id
        self.harry_client.post('/api/alert/%d/' % alert_object_id,
                               {'_method': 'PUT',
                                'user_creator': User.objects.get(username='harry').id,
                                'user': User.objects.get(username='harry').id,
                                'project': self.project_id,
                                'alert': 'harry new alert changed'})
        self.assertEqual(Alert.objects.filter(user_creator__id=str(User.objects.get(username='harry').id),
                                              alert='harry new alert',
                                              project__id=str(self.project_id)).exists(), True)
        self.assertEqual(Alert.objects.filter(user_creator__id=str(User.objects.get(username='harry').id),
                                              alert='harry new alert changed',
                                              project__id=str(self.project_id)).exists(), False)

    def __test_four__(self):
        """
        Project admin edits an Alert.
        """
        alert_object_id = Alert.objects.get(project__id=self.project_id,
                                            alert='harry new alert').id
        self.paul_client.post('/api/alert/%d/' % alert_object_id,
                              {'_method': 'PUT',
                               'user_creator': User.objects.get(username='harry').id,
                               'user': User.objects.get(username='paul').id,
                               'project': self.project_id,
                               'alert': 'harry new alert changed'})
        self.assertEqual(Alert.objects.filter(user_creator__id=str(User.objects.get(username='harry').id),
                                              alert='harry new alert',
                                              project__id=str(self.project_id)).exists(), False)
        self.assertEqual(Alert.objects.filter(user_creator__id=str(User.objects.get(username='harry').id),
                                              alert='harry new alert changed',
                                              project__id=str(self.project_id)).exists(), True)

    def __test_five__(self):
        """
        Project member removes an Alert. This should fail.
        """
        alert_object_id = Alert.objects.get(project__id=self.project_id,
                                            alert='harry new alert changed').id
        self.harry_client.post('/api/alert/%d/' % alert_object_id, {'_method': 'DELETE'})
        self.assertEqual(Alert.objects.filter(user_creator__id=str(User.objects.get(username='harry').id),
                                              alert='harry new alert changed',
                                              project__id=str(self.project_id)).exists(), True)

    def __test_six__(self):
        """
        Project admin removes an Alert.
        """
        alert_object_id = Alert.objects.get(project__id=self.project_id,
                                            alert='harry new alert changed').id
        self.paul_client.post('/api/alert/%d/' % alert_object_id, {'_method': 'DELETE'})
        self.assertEqual(Alert.objects.filter(user_creator__id=str(User.objects.get(username='harry').id),
                                              alert='harry new alert changed',
                                              project__id=str(self.project_id)).exists(), False)

########################################################################################################################
# File
########################################################################################################################


class FileTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()
        self.__test_four__()
        self.__test_five__()
        self.__test_six__()

    def __test_one__(self):
        """
        Non project member adds a file. This should fail.
        """
        self.james_client.post('/api/file/', {'project': self.project_id,
                                              'title': 'james new file'})
        self.assertEqual(File.objects.filter(user_creator__id=str(User.objects.get(username='james').id),
                                             project__id=str(self.project_id)).exists(), False)

    def __test_two__(self):
        """
        Project member adds a file.
        """
        self.paul_client.post('/api/file/', {'project': self.project_id,
                                             'title': 'paul new file'})
        self.assertEqual(File.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new file',
                                             project__id=str(self.project_id)).exists(), True)

    def __test_three__(self):
        """
        Project member edits a file. This should fail.
        """
        file_object_id = File.objects.get(project__id=self.project_id,
                                          title='paul new file').id
        self.harry_client.post('/api/file/%d/' % file_object_id, {'_method': 'PUT',
                                                                  'user': User.objects.get(username='paul').id,
                                                                  'project': self.project_id,
                                                                  'title': 'harry new file'})
        self.assertEqual(File.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new file',
                                             project__id=str(self.project_id)).exists(), True)
        self.assertEqual(File.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='harry new file',
                                             project__id=str(self.project_id)).exists(), False)

    def __test_four__(self):
        """
        Project admin edits a file.
        """
        file_object_id = File.objects.get(project__id=self.project_id,
                                          title='paul new file').id
        self.paul_client.post('/api/file/%d/' % file_object_id, {'_method': 'PUT',
                                                                 'user': User.objects.get(username='paul').id,
                                                                 'project': self.project_id,
                                                                 'title': 'test test test'})
        self.assertEqual(File.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new file',
                                             project__id=str(self.project_id)).exists(), False)
        self.assertEqual(File.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='test test test',
                                             project__id=str(self.project_id)).exists(), True)

    def __test_five__(self):
        """
        Project member removes a file. This should fail.
        """
        file_object_id = File.objects.get(project__id=self.project_id,
                                          title='test test test').id
        self.harry_client.post('/api/file/%d/' % file_object_id, {'_method': 'DELETE'})
        self.assertEqual(File.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='test test test',
                                             project__id=str(self.project_id),
                                             is_active=True).exists(), True)

    def __test_six__(self):
        """
        Project admin removes a file.
        """
        file_object_id = File.objects.get(project__id=self.project_id,
                                          title='test test test').id
        self.paul_client.post('/api/file/%d/' % file_object_id, {'_method': 'DELETE'})
        self.assertEqual(File.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='test test test',
                                             is_active=True).exists(), False)

########################################################################################################################
# Discussion
########################################################################################################################


class DiscussionTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()
        self.__test_four__()
        self.__test_five__()
        self.__test_six__()

    def __test_one__(self):
        """
        Non project member adds a discussion. This should fail.
        """
        self.james_client.post('/api/discussion/', {'project': self.project_id,
                                                    'title': 'james new discussion'})
        self.assertEqual(Discussion.objects.filter(user_creator__id=str(User.objects.get(username='james').id),
                                                   project__id=str(self.project_id)).exists(), False)

    def __test_two__(self):
        """
        Project member adds a discussion.
        """
        self.paul_client.post('/api/discussion/', {'project': self.project_id,
                                                   'title': 'paul new discussion'})
        self.assertEqual(Discussion.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                   title='paul new discussion',
                                                   project__id=str(self.project_id)).exists(), True)

    def __test_three__(self):
        """
        Project member edits a discussion. This should fail.
        """
        discussion_object_id = Discussion.objects.get(project__id=self.project_id,
                                                      title='paul new discussion').id
        self.harry_client.post('/api/discussion/%d/' % discussion_object_id,
                               {'_method': 'PUT',
                                'user': User.objects.get(username='paul').id,
                                'project': self.project_id,
                                'title': 'harry new file'})
        self.assertEqual(Discussion.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                   title='paul new discussion',
                                                   project__id=str(self.project_id)).exists(), True)
        self.assertEqual(Discussion.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                   title='harry new discussion',
                                                   project__id=str(self.project_id)).exists(), False)

    def __test_four__(self):
        """
        Project admin edits a discussion.
        """
        discussion_object_id = Discussion.objects.get(project__id=self.project_id,
                                                      title='paul new discussion').id
        self.paul_client.post('/api/discussion/%d/' % discussion_object_id,
                              {'_method': 'PUT',
                               'user': User.objects.get(username='paul').id,
                               'project': self.project_id,
                               'title': 'test test test'})
        self.assertEqual(Discussion.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                   title='paul new discussion',
                                                   project__id=str(self.project_id)).exists(), False)
        self.assertEqual(Discussion.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                   title='test test test',
                                                   project__id=str(self.project_id)).exists(), True)

    def __test_five__(self):
        """
        Project member removes a discussion. This should fail.
        """
        discussion_object_id = Discussion.objects.get(project__id=self.project_id,
                                                      title='test test test').id
        self.harry_client.post('/api/discussion/%d/' % discussion_object_id, {'_method': 'DELETE'})
        self.assertEqual(Discussion.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                   title='test test test',
                                                   project__id=str(self.project_id),
                                                   is_active=True).exists(), True)

    def __test_six__(self):
        """
        Project admin removes a discussion.
        """
        discussion_object_id = Discussion.objects.get(project__id=self.project_id,
                                                      title='test test test').id
        self.paul_client.post('/api/discussion/%d/' % discussion_object_id, {'_method': 'DELETE'})
        self.assertEqual(Discussion.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                   title='test test test',
                                                   is_active=True).exists(), False)

########################################################################################################################
# Comment
########################################################################################################################


class CommentTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()
        self.__test_four__()
        self.__test_five__()
        self.__test_six__()

    def __test_one__(self):
        """
        Non project member adds a discussion. This should fail. This function also creates a test discussion to add
        comment to.
        """
        self.paul_client.post('/api/discussion/', {'project': self.project_id,
                                                   'title': 'paul new discussion'})
        self.assertEqual(Discussion.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                   title='paul new discussion',
                                                   project__id=str(self.project_id)).exists(), True)
        self.james_client.post('/api/comment/', {'project': self.project_id,
                                                 'discussion': Discussion.objects.get(title='paul new discussion').id,
                                                 'comment_text': 'james new comment'})
        self.assertEqual(Comment.objects.filter(user_creator__id=str(User.objects.get(username='james').id),
                                                project__id=str(self.project_id)).exists(), False)

    def __test_two__(self):
        """
        Project member adds a comment.
        """
        self.paul_client.post('/api/comment/', {'project': self.project_id,
                                                'discussion': Discussion.objects.get(title='paul new discussion').id,
                                                'comment_text': 'paul new comment'})
        self.assertEqual(Comment.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                comment_text='paul new comment',
                                                project__id=str(self.project_id)).exists(), True)

    def __test_three__(self):
        """
        Project member edits a comment. This should fail.
        """
        comment_object_id = Comment.objects.get(project__id=self.project_id,
                                                comment_text='paul new comment').id
        self.harry_client.post('/api/comment/%d/' % comment_object_id,
                               {'_method': 'PUT',
                                'user': User.objects.get(username='paul').id,
                                'project': self.project_id,
                                'discussion': Discussion.objects.get(title='paul new discussion').id,
                                'comment_text': 'harry new comment'})
        self.assertEqual(Comment.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                comment_text='paul new comment',
                                                project__id=str(self.project_id)).exists(), True)
        self.assertEqual(Comment.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                comment_text='harry new comment',
                                                project__id=str(self.project_id)).exists(), False)

    def __test_four__(self):
        """
        Project admin edits a comment.
        """
        comment_object_id = Comment.objects.get(project__id=self.project_id,
                                                comment_text='paul new comment').id
        self.paul_client.post('/api/comment/%d/' % comment_object_id,
                              {'_method': 'PUT',
                               'user': User.objects.get(username='paul').id,
                               'project': self.project_id,
                               'discussion': Discussion.objects.get(title='paul new discussion').id,
                               'comment_text': 'test test test'})
        self.assertEqual(Comment.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                comment_text='paul new comment',
                                                project__id=str(self.project_id)).exists(), False)
        self.assertEqual(Comment.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                comment_text='test test test',
                                                project__id=str(self.project_id)).exists(), True)

    def __test_five__(self):
        """
        Project member removes a comment. This should fail.
        """
        comment_object_id = Comment.objects.get(project__id=self.project_id,
                                                comment_text='test test test').id
        self.harry_client.post('/api/comment/%d/' % comment_object_id, {'_method': 'DELETE'})
        self.assertEqual(Comment.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                comment_text='test test test',
                                                project__id=str(self.project_id),
                                                is_active=True).exists(), True)

    def __test_six__(self):
        """
        Project admin removes a comment.
        """
        comment_object_id = Comment.objects.get(project__id=self.project_id,
                                                comment_text='test test test').id
        self.paul_client.post('/api/comment/%d/' % comment_object_id, {'_method': 'DELETE'})
        self.assertEqual(Comment.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                comment_text='test test test',
                                                is_active=True).exists(), False)

########################################################################################################################
# Blog
########################################################################################################################


class BlogTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()
        self.__test_four__()
        self.__test_five__()
        self.__test_six__()

    def __test_one__(self):
        """
        Non project member adds a blog. This should fail.
        """
        self.james_client.post('/api/blog/', {'project': self.project_id,
                                              'title': 'james new blog'})
        self.assertEqual(Blog.objects.filter(user_creator__id=str(User.objects.get(username='james').id),
                                             project__id=str(self.project_id)).exists(), False)

    def __test_two__(self):
        """
        Project member adds a blog.
        """
        self.paul_client.post('/api/blog/', {'project': self.project_id,
                                             'title': 'paul new blog'})
        self.assertEqual(Blog.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new blog',
                                             project__id=str(self.project_id)).exists(), True)

    def __test_three__(self):
        """
        Project member edits a blog. This should fail.
        """
        blog_object_id = Blog.objects.get(project__id=self.project_id,
                                          title='paul new blog').id
        self.harry_client.post('/api/blog/%d/' % blog_object_id, {'_method': 'PUT',
                                                                  'user': User.objects.get(username='paul').id,
                                                                  'project': self.project_id,
                                                                  'title': 'harry new blog'})
        self.assertEqual(Blog.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new blog',
                                             project__id=str(self.project_id)).exists(), True)
        self.assertEqual(Blog.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='harry new blog',
                                             project__id=str(self.project_id)).exists(), False)

    def __test_four__(self):
        """
        Project admin edits a blog.
        """
        blog_object_id = Blog.objects.get(project__id=self.project_id,
                                          title='paul new blog').id
        self.paul_client.post('/api/blog/%d/' % blog_object_id, {'_method': 'PUT',
                                                                 'user': User.objects.get(username='paul').id,
                                                                 'project': self.project_id,
                                                                 'title': 'test test test'})
        self.assertEqual(Blog.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new blog',
                                             project__id=str(self.project_id)).exists(), False)
        self.assertEqual(Blog.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='test test test',
                                             project__id=str(self.project_id)).exists(), True)

    def __test_five__(self):
        """
        Project member removes a blog. This should fail.
        """
        blog_object_id = Blog.objects.get(project__id=self.project_id,
                                          title='test test test').id
        self.harry_client.post('/api/blog/%d/' % blog_object_id, {'_method': 'DELETE'})
        self.assertEqual(Blog.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='test test test',
                                             project__id=str(self.project_id),
                                             is_active=True).exists(), True)

    def __test_six__(self):
        """
        Project admin removes a blog.
        """
        blog_object_id = Blog.objects.get(project__id=self.project_id,
                                          title='test test test').id
        self.paul_client.post('/api/blog/%d/' % blog_object_id, {'_method': 'DELETE'})
        self.assertEqual(Blog.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='test test test',
                                             is_active=True).exists(), False)

########################################################################################################################
# BlogPost
########################################################################################################################


class BlogPostTestCase(GenericTestCase):
    def tests(self):
        self.__test_one__()
        self.__test_two__()
        self.__test_three__()
        self.__test_four__()
        self.__test_five__()
        self.__test_six__()

    def __test_one__(self):
        """
        Non project member adds a BlogPost. This should fail. This function also creates a test Blog to add
        BlogPosts to.
        """
        self.paul_client.post('/api/blog/', {'project': self.project_id,
                                             'title': 'paul new blog'})
        self.assertEqual(Blog.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                             title='paul new blog',
                                             project__id=str(self.project_id)).exists(), True)
        self.james_client.post('/api/blog_post/', {'project': self.project_id,
                                                   'blog': Blog.objects.get(title='paul new blog').id,
                                                   'post': 'james new post'})
        self.assertEqual(BlogPost.objects.filter(user_creator__id=str(User.objects.get(username='james').id),
                                                 blog__id=str(Blog.objects.get(title='paul new blog').id)).exists(),
                         False)

    def __test_two__(self):
        """
        Project member adds a BlogPost.
        """
        self.paul_client.post('/api/blog_post/', {'project': self.project_id,
                                                  'blog': Blog.objects.get(title='paul new blog').id,
                                                  'post': 'paul new post'})
        self.assertEqual(BlogPost.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                 post='paul new post',
                                                 blog__id=str(Blog.objects.get(title='paul new blog').id)).exists(),
                         True)

    def __test_three__(self):
        """
        Project member edits a BlogPost. This should fail.
        """
        blogpost_object_id = BlogPost.objects.get(blog__id=Blog.objects.get(title='paul new blog').id,
                                                  post='paul new post').id
        self.harry_client.post('/api/blog_post/%d/' % blogpost_object_id,
                               {'_method': 'PUT',
                                'project': self.project_id,
                                'user': User.objects.get(username='paul').id,
                                'blog': Blog.objects.get(title='paul new blog').id,
                                'post': 'harry new post'})
        self.assertEqual(BlogPost.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                 post='paul new post',
                                                 blog__id=str(Blog.objects.get(title='paul new blog').id)).exists(),
                         True)
        self.assertEqual(BlogPost.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                 post='harry new post',
                                                 blog__id=str(Blog.objects.get(title='paul new blog').id)).exists(),
                         False)

    def __test_four__(self):
        """
        Project admin edits a BlogPost.
        """
        blogpost_object_id = BlogPost.objects.get(blog__id=Blog.objects.get(title='paul new blog').id,
                                                  post='paul new post').id
        self.paul_client.post('/api/blog_post/%d/' % blogpost_object_id,
                              {'_method': 'PUT',
                               'project': self.project_id,
                               'user': User.objects.get(username='paul').id,
                               'blog': Blog.objects.get(title='paul new blog').id,
                               'post': 'test test test'})
        self.assertEqual(BlogPost.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                 post='paul new post',
                                                 blog__id=str(Blog.objects.get(title='paul new blog').id)).exists(),
                         False)
        self.assertEqual(BlogPost.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                 post='test test test',
                                                 blog__id=str(Blog.objects.get(title='paul new blog').id)).exists(),
                         True)

    def __test_five__(self):
        """
        Project member removes a BlogPost. This should fail.
        """
        blogpost_object_id = BlogPost.objects.get(blog__id=Blog.objects.get(title='paul new blog').id,
                                                  post='test test test').id
        self.harry_client.post('/api/blog_post/%d/' % blogpost_object_id, {'_method': 'DELETE'})
        self.assertEqual(BlogPost.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                 post='test test test',
                                                 blog__id=str(Blog.objects.get(title='paul new blog').id),
                                                 is_active=True).exists(), True)

    def __test_six__(self):
        """
        Project admin removes a BlogPost.
        """
        blogpost_object_id = BlogPost.objects.get(blog__id=Blog.objects.get(title='paul new blog').id,
                                                  post='test test test').id
        self.paul_client.post('/api/blog_post/%d/' % blogpost_object_id, {'_method': 'DELETE'})
        self.assertEqual(BlogPost.objects.filter(user_creator__id=str(User.objects.get(username='paul').id),
                                                 post='test test test',
                                                 is_active=True).exists(), False)
