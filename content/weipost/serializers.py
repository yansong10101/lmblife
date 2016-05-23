from rest_framework import serializers
from content.weipost.models import JieJiPost, JieJiComment, PostTag
from core.serializers import (UniversityRetrieveSerializer, CustomerRetrieveSerializer, OrgAdminRetrieveSerializer)


class JieJiPostListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:jie-ji-post-get')
    author = CustomerRetrieveSerializer(read_only=True, allow_null=True)
    admin = OrgAdminRetrieveSerializer(read_only=True, allow_null=True)
    mentioned = CustomerRetrieveSerializer(read_only=True, allow_null=True, many=True)

    class Meta:
        model = JieJiPost
        fields = ('url', 'pk', 'post_subject', 'post_message', 'created_date', 'like_count', 'author', 'admin',
                  'mentioned', )


class JieJiPostRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    university = UniversityRetrieveSerializer(read_only=True)
    author = CustomerRetrieveSerializer(read_only=True, allow_null=True)
    admin = OrgAdminRetrieveSerializer(read_only=True, allow_null=True)
    mentioned = CustomerRetrieveSerializer(read_only=True, allow_null=True, many=True)

    class Meta:
        model = JieJiPost
        fields = ('pk', 'post_subject', 'post_message', 'created_date', 'like_count', 'university', 'author', 'admin',
                  'mentioned', )


class JieJiCommentListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:jie-ji-comment-get')
    user = CustomerRetrieveSerializer(read_only=True, allow_null=True)
    admin = OrgAdminRetrieveSerializer(read_only=True, allow_null=True)
    mentioned = CustomerRetrieveSerializer(read_only=True, allow_null=True, many=True)

    class Meta:
        model = JieJiComment
        fields = ('url', 'pk', 'post', 'created_date', 'comment_message', 'like_count', 'user', 'admin', 'mentioned', )


class JieJiCommentRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    author = CustomerRetrieveSerializer(read_only=True, allow_null=True)
    admin = OrgAdminRetrieveSerializer(read_only=True, allow_null=True)
    mentioned = CustomerRetrieveSerializer(read_only=True, allow_null=True, many=True)

    class Meta:
        model = JieJiComment
        fields = ('pk', 'post', 'created_date', 'comment_message', 'like_count', 'author', 'admin', 'mentioned', )
