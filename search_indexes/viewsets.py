from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_TERMS,
    LOOKUP_FILTER_RANGE,
    LOOKUP_FILTER_PREFIX,
    LOOKUP_FILTER_WILDCARD,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    LOOKUP_QUERY_EXCLUDE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    IdsFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
    NestedFilteringFilterBackend,
    SuggesterFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from .documents.users import ProfileDocument
from .serializers.users import UsersDocumentSerializer

class UsersDocumentViewSet(BaseDocumentViewSet):
    document = ProfileDocument
    serializer_class = UsersDocumentSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        IdsFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        NestedFilteringFilterBackend,
        SuggesterFilterBackend,
    ]
    search_fields = {
        'display_name',
        'about',
        'user.username',
    }
    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'display_name': 'display_name.raw',
        'about': 'about.raw',
        'username': 'user.username.raw',
    }
    ordering_fields = {
        'id': 'id',
        'display_name': 'display_name.raw',
        'about': 'about.raw',
        'username': 'user.username.raw',
    }
    nested_filter_fields = {
        'username': {
            'field': 'user.username.raw',
            'path': 'user',
        }
    }
    suggester_fields = {
        'display_name_suggest': {
            'field': 'display_name.suggest',
            'suggesters': [
                'SUGGESTER_COMPLETION',
            ],
        },
        'about_suggest': {
            'field': 'about.suggest',
            'suggesters': [
                'SUGGESTER_COMPLETION',
            ],
        },
        'username_suggest': {
            'field': 'user.username.suggest',
            'suggesters': [
                'SUGGESTER_COMPLETION',
            ],
        },
    }
