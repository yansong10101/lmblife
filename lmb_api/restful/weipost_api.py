from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from content.weipost.serializers import (JieJiPost, JieJiComment, JieJiPostListSerializer, JieJiPostRetrieveSerializer,
                                         JieJiCommentListSerializer, JieJiCommentRetrieveSerializer)


class JieJiPostList(ListAPIView):
    queryset = JieJiPost.objects
    serializer_class = JieJiPostListSerializer
    paginate_by = 15


class JieJiPostRetrieve(RetrieveAPIView):
    queryset = JieJiPost.objects
    serializer_class = JieJiPostRetrieveSerializer


class JieJiCommentList(ListAPIView):
    queryset = JieJiComment.objects
    serializer_class = JieJiCommentListSerializer
    paginate_by = 15


class JieJiCommentRetrieve(RetrieveAPIView):
    queryset = JieJiComment.objects
    serializer_class = JieJiCommentRetrieveSerializer
