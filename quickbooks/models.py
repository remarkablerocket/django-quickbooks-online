from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
try:
    from django_extensions.db.fields.encrypted import EncryptedCharField
except ImportError:
    from django_fields.fields import EncryptedCharField


class QuickbooksToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    access_token = EncryptedCharField(max_length=255)
    access_token_secret = EncryptedCharField(max_length=255)
    realm_id = models.CharField(max_length=64)
    data_source = models.CharField(max_length=10)


class MissingTokenException(Exception):
    pass


def find_quickbooks_token(request_or_user):
    if isinstance(request_or_user, get_user_model()):
        user = request_or_user
    else:
        user = request_or_user.user
    if not user.is_authenticated():
        return None
    try:
        return QuickbooksToken.objects.filter(user=user)[0]
    except IndexError:
        return None


def get_quickbooks_token(request):
    token = find_quickbooks_token(request)
    if token is None:
        raise MissingTokenException("No QuickBooks OAuth token exists for this user")
    return token
