from core.models import University
from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.pagination import CursorPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from content.weipost.serializers import (JieJiPost, JieJiComment, JieJiPostListSerializer, JieJiPostRetrieveSerializer,
                                         JieJiCommentListSerializer, JieJiCommentRetrieveSerializer, PostTag)
from content.weipost.forms import PostCreationForm, CommentCreationForm
from lmb_api.utils import response_message


def request_parameter_validator(required_paras, parameter_dict):
    for para in required_paras:
        if para not in parameter_dict.keys() or not parameter_dict[para]:
            return False
    return True


class CustomJieJiPostPagination(CursorPagination):
    ordering = '-pk'
    # cursor_query_param = 'stamp'
    # template = None

    def paginate_queryset(self, queryset, request, view=None):
        limit = int(request.query_params['limit'])
        self.page_size = limit
        return super(CustomJieJiPostPagination, self).paginate_queryset(queryset, request)


class JieJiPostList(ListAPIView):
    queryset = JieJiPost.objects
    serializer_class = JieJiPostListSerializer
    pagination_class = CustomJieJiPostPagination

    def validate_request_parameters(self):
        required_paras = ('limit', 'org_slug')
        if not request_parameter_validator(required_paras, self.request.query_params):
            raise exceptions.ValidationError('Invalid request parameters ! ')
        return True

    def get_queryset(self):
        if self.validate_request_parameters():
            university = University.universities.get_by_slug(self.request.query_params['org_slug'])
            posts = JieJiPost.objects.filter(university=university)
            return posts


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


@api_view(['POST', ])
@parser_classes((JSONParser,))
def create_post(request):
    if request.method == 'POST':
        form = PostCreationForm(request.data)
        if form.is_valid():
            form.save()
            return Response(data=response_message(code=200), status=status.HTTP_200_OK)
        return Response(data=response_message(message='Invalid request input'), status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST', ])
@parser_classes((JSONParser,))
def create_comment(request):
    if request.method == 'POST':
        form = CommentCreationForm(request.data)
        if form.is_valid():
            form.save()
            return Response(data=response_message(code=200), status=status.HTTP_200_OK)
        return Response(data=response_message(message='Invalid request input'), status=status.HTTP_400_BAD_REQUEST)
    return Response(data=response_message(code=405), status=status.HTTP_405_METHOD_NOT_ALLOWED)
