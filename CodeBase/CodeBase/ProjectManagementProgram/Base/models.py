# Python imports
import datetime

# Django imports
from django.db import models
from django.contrib.auth.models import User


class UserExtra(models.Model):
    """
    Used to store extra fields for the User object.
    """
    user = models.OneToOneField(User, unique=True)
    company = models.CharField(max_length=60, blank=True, null=True)
    department = models.CharField(max_length=60, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return 'for user_id: %s' % self.user.id


class GenericBase(models.Model):
    """
    Abstract class for generic fields that a lot of database classes will use.
    """
    user_creator = models.ForeignKey(User, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    user_last_modified = models.ForeignKey(User, related_name='user_last_modified', blank=True, null=True)
    last_modified = models.DateField(blank=True, null=True)
    user_closed = models.ForeignKey(User, related_name='user_closed', blank=True, null=True)
    date_closed = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        """
        Overrides default behaviour so object is not deleted but set to is_active is False.
        """
        self.is_active = False
        self.save()


class Project(models.Model):
    """
    Main project table.
    """
    title = models.CharField(max_length=60, blank=True, null=True)
    homepage_text = models.TextField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title

    def delete(self, *args, **kwargs):
        """
        Overrides default behaviour so object is not deleted but set to is_active is False.
        """
        self.is_active = False
        self.save()


class UserProject(models.Model):
    """
    Special many to many table created due to extra fields needed.
    """
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    is_creator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "for user_id:%s and project_id %s" % (self.user.id, self.project.id)

    def delete(self, *args, **kwargs):
        """
        Overrides default behaviour so object is not deleted but set to is_active is False.
        """
        self.is_active = False
        self.save()


class Link(GenericBase):
    """
    Stores project Links.
    """
    project = models.ForeignKey(Project)
    title = models.TextField()
    link_text = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.project.title

    def save(self, *args, **kwargs):
        returned_object = super(Link, self).save(*args, **kwargs)
        if self.user_last_modified:
            user_creator = self.user_last_modified
        else:
            user_creator = self.user_creator
        project = self.project
        alert = "(%s) %s %s added a new link to %s" % (datetime.datetime.now().date().isoformat(),
                                                       user_creator.first_name,
                                                       user_creator.last_name,
                                                       project.title)
        alert_object = Alert(user_creator=user_creator, project=project, alert=alert)
        alert_object.save()
        return returned_object


class Alert(models.Model):
    """
    Stores project alerts. An alert is created when ANY action is performed on a project. For example adding a file.
    """
    project = models.ForeignKey(Project)
    alert = models.TextField()
    user_creator = models.ForeignKey(User)
    date_created = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.project.title


class File(GenericBase):
    """
    Stores project files. For example pdf or ms word (.doc) files.
    """
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.user_last_modified:
            user_creator = self.user_last_modified
        else:
            user_creator = self.user_creator
        project = self.project
        alert = "(%s) %s %s added a new file to %s" % (datetime.datetime.now().date().isoformat(),
                                                       user_creator.first_name,
                                                       user_creator.last_name,
                                                       project.title)
        alert_object = Alert(user_creator=user_creator, project=project, alert=alert)
        alert_object.save()
        super(File, self).save(*args, **kwargs)


class Discussion(GenericBase):
    """
    Stores project discussions. Comments can be added to a discussion and discussions can be closed with a conclusion.
    """
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=60, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.user_last_modified:
            user_creator = self.user_last_modified
        else:
            user_creator = self.user_creator
        project = self.project
        alert = "(%s) %s %s added a new discussion to %s" % (datetime.datetime.now().date().isoformat(),
                                                             user_creator.first_name,
                                                             user_creator.last_name,
                                                             project.title)
        alert_object = Alert(user_creator=user_creator, project=project, alert=alert)
        alert_object.save()
        super(Discussion, self).save(*args, **kwargs)


class Comment(GenericBase):
    """
    Stores discussion comments.
    """
    project = models.ForeignKey(Project)
    discussion = models.ForeignKey(Discussion)
    comment_text = models.TextField()

    def __unicode__(self):
        return "comment for discussion_id: %s" % self.project.id

    def save(self, *args, **kwargs):
        if self.user_last_modified:
            user_creator = self.user_last_modified
        else:
            user_creator = self.user_creator
        project = self.project
        alert = "(%s) %s %s added a new comment to %s" % (datetime.datetime.now().date().isoformat(),
                                                          user_creator.first_name,
                                                          user_creator.last_name,
                                                          project.title)
        alert_object = Alert(user_creator=user_creator, project=project, alert=alert)
        alert_object.save()
        super(Comment, self).save(*args, **kwargs)


class Blog(GenericBase):
    """
    Stores the project blog. One blog can be added to a project by admins.
    """
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=60, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "blog for project_id:%s" % self.project.id

    def save(self, *args, **kwargs):
        if self.user_last_modified:
            user_creator = self.user_last_modified
        else:
            user_creator = self.user_creator
        project = self.project
        alert = "(%s) %s %s added a new blog to %s" % (datetime.datetime.now().date().isoformat(),
                                                       user_creator.first_name,
                                                       user_creator.last_name,
                                                       project.title)
        alert_object = Alert(user_creator=user_creator, project=project, alert=alert)
        alert_object.save()
        super(Blog, self).save(*args, **kwargs)


class BlogPost(GenericBase):
    """
    Stores posts for the project blog.
    """
    project = models.ForeignKey(Project)
    blog = models.ForeignKey(Blog)
    parent_entry = models.ForeignKey("self", blank=True, null=True)
    post = models.TextField()

    def __unicode__(self):
        return "for blog_id:%s" % self.blog.id

    def save(self, *args, **kwargs):
        if self.user_last_modified:
            user_creator = self.user_last_modified
        else:
            user_creator = self.user_creator
        project = self.blog.project
        alert = "(%s) %s %s added a new blog post to %s" % (datetime.datetime.now().date().isoformat(),
                                                            user_creator.first_name,
                                                            user_creator.last_name,
                                                            project.title)
        alert_object = Alert(user_creator=user_creator, project=project, alert=alert)
        alert_object.save()
        super(BlogPost, self).save(*args, **kwargs)
