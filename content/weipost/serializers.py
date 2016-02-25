from rest_framework import serializers
from content.weipost.models import JieJiPost, JieJiComment
from core.serializers import (FeatureRetrieveSerializer, UniversityRetrieveSerializer, CustomerRetrieveSerializer,
                              OrgAdminRetrieveSerializer)


class JieJiPostListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:jie-ji-post-get')

    class Meta:
        model = JieJiPost
        fields = ('url', 'pk', 'post_subject', 'post_message', 'created_date', 'comments_count', 'like_count', )


class JieJiPostRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    feature = FeatureRetrieveSerializer(read_only=True)
    university = UniversityRetrieveSerializer(read_only=True)
    user = CustomerRetrieveSerializer(read_only=True, allow_null=True)
    admin = OrgAdminRetrieveSerializer(read_only=True, allow_null=True)

    class Meta:
        model = JieJiPost
        fields = ('pk', 'post_subject', 'post_message', 'created_date', 'comments_count', 'like_count', 'feature',
                  'university', 'user', 'admin', )


class JieJiCommentListSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:jie-ji-comment-get')
    user = CustomerRetrieveSerializer(read_only=True, allow_null=True)
    admin = OrgAdminRetrieveSerializer(read_only=True, allow_null=True)

    class Meta:
        model = JieJiComment
        fields = ('url', 'pk', 'post', 'created_date', 'comment_message', 'like_count', 'user', 'admin', )


class JieJiCommentRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    user = CustomerRetrieveSerializer(read_only=True, allow_null=True)
    admin = OrgAdminRetrieveSerializer(read_only=True, allow_null=True)

    class Meta:
        model = JieJiComment
        fields = ('pk', 'post', 'created_date', 'comment_message', 'like_count', 'user', 'admin', )
