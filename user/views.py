"""
User views
"""
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serialisers import AuthTokenSerializer


class CreateTokenView(ObtainAuthToken):
    """Createnew auth token"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
