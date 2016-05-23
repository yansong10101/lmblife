from django.db import models
from core.models import University, Feature, Customer, OrgAdmin


class PostTag(models.Model):
    tag_name = models.CharField(max_length=255, unique=True)
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_date = models.DateTimeField(auto_now=True, editable=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.tag_name


class AbstractWeiPost(models.Model):
    university = models.ForeignKey(University, related_name='wei_post_university')
    author = models.ForeignKey(Customer, related_name='wei_post_author', null=True)
    admin = models.ForeignKey(OrgAdmin, related_name='wei_post_admin', null=True)
    mentioned = models.ManyToManyField(Customer, related_name='wei_port_mentioned')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_date = models.DateTimeField(auto_now=True, editable=False)
    is_edited = models.BooleanField(default=False)
    post_subject = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    post_message = models.TextField()
    comments_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)

    class Meta:
        abstract = True


class AbstractWeiComment(models.Model):
    """
        Note:
        Comment Concrete Class should have FK for corresponding Concrete Post class
    """
    author = models.ForeignKey(Customer, related_name='wei_comment_author', null=True)
    admin = models.ForeignKey(OrgAdmin, related_name='wei_comment_admin', null=True)
    mentioned = models.ManyToManyField(Customer, related_name='wei_comment_mentioned')
    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    last_modified_date = models.DateTimeField(auto_now=True, editable=False)
    is_edited = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    comment_message = models.TextField()
    like_count = models.IntegerField(default=0)

    class Meta:
        abstract = True


class JieJiPost(AbstractWeiPost):
    post_tag = models.ManyToManyField(PostTag, related_name='jie_ji_post_post_tag')

    def __str__(self):
        return self.post_message


class JieJiComment(AbstractWeiComment):
    post = models.ForeignKey(JieJiPost, related_name='jie_ji_post')

    def __str__(self):
        return self.comment_message
