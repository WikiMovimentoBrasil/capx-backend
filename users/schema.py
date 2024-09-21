from drf_spectacular.extensions import OpenApiViewExtension, OpenApiSerializerExtension
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, PolymorphicProxySerializer
from rest_social_auth.serializers import UserKnoxSerializer, KnoxSerializer

class SocialKnox(OpenApiSerializerExtension):
    target_class = 'rest_social_auth.serializers.KnoxSerializer'

    def map_serializer(self, auto_schema, direction):
        return {
            'type': 'object',
            'properties': {
                'provider': {
                    'type': 'string',
                    'description': 'Name of the social media provider.',
                    'enum': ['mediawiki'],
                },
            },
            'required': ['provider'],
        }

class SocialKnoxLogin(OpenApiViewExtension):
    target_class = 'rest_social_auth.views.SocialKnoxOnlyAuthView'

    def view_replacement(self):
        class Fixed(self.target_class):
            @extend_schema(
                summary='Request oauth token from social media provider.',
                description='This endpoint requests an OAuth token from the social media provider.',
                request=KnoxSerializer,
                responses={(200, 'application/json'): {
                    'type': 'object',
                    'properties': {
                        'oauth_token': {
                            'type': 'string',
                            'description': 'OAuth token.',
                        },
                        'oauth_token_secret': {
                            'type': 'string',
                            'description': 'OAuth token secret.',
                        },
                        'oauth_callback_confirmed': {
                            'type': 'string',
                            'description': 'OAuth callback confirmed.',
                        }
                    },
                }},
            )
            def post(self, request, *args, **kwargs):
                return super().post(request, *args, **kwargs)
        
        return Fixed

class UserKnox(OpenApiSerializerExtension):
    target_class = 'rest_social_auth.serializers.UserKnoxSerializer'

    def map_serializer(self, auto_schema, direction):
        return {
            'type': 'object',
            'properties': {
                'provider': {
                    'type': 'string',
                    'description': 'Name of the social media provider.',
                    'enum': ['mediawiki'],
                },
                'oauth_token': {
                    'type': 'string',
                    'description': 'OAuth token.',
                },
                'oauth_token_secret': {
                    'type': 'string',
                    'description': 'OAuth token secret.',
                },
                'oauth_verifier': {
                    'type': 'string',
                    'description': 'OAuth verifier received by the provider.',
                },
            },
            'required': ['provider', 'oauth_token', 'oauth_token_secret', 'oauth_verifier'],
        }

class UserKnoxLogin(OpenApiViewExtension):
    target_class = 'rest_social_auth.views.SocialKnoxUserAuthView'

    def view_replacement(self):
        class Fixed(self.target_class):
            @extend_schema(
                summary='Request authentication token from social media provider.',
                description='This endpoint logs in a user with social media credentials.',
                request=UserKnoxSerializer,
                responses={(200, 'application/json'): {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                            'description': 'User ID on the database.',
                        },
                        'token': {
                            'type': 'string',
                            'description': 'Authentication token.',
                        },
                        'username': {
                            'type': 'string',
                            'description': 'Username as registered by the provider.',
                        },
                        'email': {
                            'type': 'string',
                            'description': 'Email as registered by the provider. Not implemented.',
                        },
                        'user_groups': {
                            'type': 'array',
                            'nullable': True,
                            'items': {
                                'type': 'string',
                            },
                            'description': 'Groups the user belongs to. Not implemented.',
                        }
                    },
                }},
            )
            def post(self, request, *args, **kwargs):
                return super().post(request, *args, **kwargs)
        
        return Fixed

