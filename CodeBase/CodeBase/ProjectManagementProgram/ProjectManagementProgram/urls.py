from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework.urlpatterns import format_suffix_patterns
from Base.views import UserList
from Base.views import UserDetail
from Base.views import UserExtraList
from Base.views import UserExtraDetail
from Base.views import ProjectList
from Base.views import ProjectDetail
from Base.views import UserProjectList
from Base.views import UserProjectDetail
from Base.views import LinkList
from Base.views import LinkDetail
from Base.views import AlertList
from Base.views import AlertDetail
from Base.views import FileList
from Base.views import FileDetail
from Base.views import DiscussionList
from Base.views import DiscussionDetail
from Base.views import CommentList
from Base.views import CommentDetail
from Base.views import BlogList
from Base.views import BlogDetail
from Base.views import BlogPostList
from Base.views import BlogPostDetail


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'ProjectManagementProgram.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       )

# User
urlpatterns += patterns('',
                        url(r'^api/user/$', UserList.as_view()),
                        url(r'^api/user/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
                        )

# UserExtra
urlpatterns += patterns('',
                        url(r'^api/user_extra/$', UserExtraList.as_view()),
                        url(r'^api/user_extra/(?P<pk>[0-9]+)/$', UserExtraDetail.as_view()),
                        )

# Project
urlpatterns += patterns('',
                        url(r'^api/project/$', ProjectList.as_view()),
                        url(r'^api/project/(?P<pk>[0-9]+)/$', ProjectDetail.as_view()),
                        )

# UserProject
urlpatterns += patterns('',
                        url(r'^api/user_project/$', UserProjectList.as_view()),
                        url(r'^api/user_project/(?P<pk>[0-9]+)/$', UserProjectDetail.as_view()),
                        )

# Link
urlpatterns += patterns('',
                        url(r'^api/link/$', LinkList.as_view()),
                        url(r'^api/link/(?P<pk>[0-9]+)/$', LinkDetail.as_view()),
                        )

# Alert
urlpatterns += patterns('',
                        url(r'^api/alert/$', AlertList.as_view()),
                        url(r'^api/alert/(?P<pk>[0-9]+)/$', AlertDetail.as_view()),
                        )

# File
urlpatterns += patterns('',
                        url(r'^api/file/$', FileList.as_view()),
                        url(r'^api/file/(?P<pk>[0-9]+)/$', FileDetail.as_view()),
                        )

# Discussion
urlpatterns += patterns('',
                        url(r'^api/discussion/$', DiscussionList.as_view()),
                        url(r'^api/discussion/(?P<pk>[0-9]+)/$', DiscussionDetail.as_view()),
                        )

# Comment
urlpatterns += patterns('',
                        url(r'^api/comment/$', CommentList.as_view()),
                        url(r'^api/comment/(?P<pk>[0-9]+)/$', CommentDetail.as_view()),
                        )

# Blog
urlpatterns += patterns('',
                        url(r'^api/blog/$', BlogList.as_view()),
                        url(r'^api/blog/(?P<pk>[0-9]+)/$', BlogDetail.as_view()),
                        )

# BlogPost
urlpatterns += patterns('',
                        url(r'^api/blog_post/$', BlogPostList.as_view()),
                        url(r'^api/blog_post/(?P<pk>[0-9]+)/$', BlogPostDetail.as_view()),
                        )

urlpatterns = format_suffix_patterns(urlpatterns)