from django import forms
from content.weipost.models import JieJiPost, JieJiComment, PostTag, Customer, University
from lmb_api.utils import get_cached_customer_or_admin_by_token


def split_list_parameter(para_value, separator):
    return para_value.split(separator)


class PostCreationForm(forms.Form):
    org_slug = forms.CharField()
    token = forms.CharField()
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    def get_author(self):
        token = self.cleaned_data['token']
        return get_cached_customer_or_admin_by_token(token)

    def get_university(self):
        slug = self.cleaned_data['org_slug']
        return University.universities.get_by_slug(slug)

    def save(self):
        post = JieJiPost()
        author = self.get_author()
        if isinstance(author, Customer):
            post.author = author
            post.admin = None
        else:
            post.author = None
            post.admin = author
        post.post_subject = self.cleaned_data['subject']
        post.post_message = self.cleaned_data['content']
        university = self.get_university()
        post.university = university
        post.save()
        return post


class CommentCreationForm(forms.Form):
    token = forms.CharField()
    post_id = forms.IntegerField()
    mention_ids = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

    def get_author(self):
        token = self.cleaned_data['token']
        return get_cached_customer_or_admin_by_token(token)

    def get_post(self):
        post_id = int(self.cleaned_data['post_id'])
        return JieJiPost.objects.get(pk=post_id)

    def get_mentioned_users(self):
        mentioned_ids = split_list_parameter(self.cleaned_data['mention_ids'], '|')
        return [Customer.customers.get_customer(pk=user_id) or None for user_id in mentioned_ids]

    def save(self):
        comment = JieJiComment()
        author = self.get_author()
        if isinstance(author, Customer):
            comment.author = author
            comment.admin = None
        else:
            comment.author = None
            comment.admin = author
        comment.comment_message = self.cleaned_data['content']
        comment.post = self.get_post()
        comment.mentioned.add(self.get_mentioned_users())
        comment.save()
        return comment
