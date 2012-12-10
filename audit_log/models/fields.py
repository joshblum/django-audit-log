from django.db import models
from django.contrib.auth.models import User
from audit_log import registration

class LastUserField(models.ForeignKey):
    """
    A field that keeps the last user that saved an instance
    of a model. None will be the value for AnonymousUser.
    """
    
    def __init__(self, to=User, null=True,  **kwargs):
        super(LastUserField, self).__init__(to=to, null=null, **kwargs)
    
    def contribute_to_class(self, cls, name):
        super(LastUserField, self).contribute_to_class(cls, name)
        registry = registration.FieldRegistry(self.__class__)
        registry.add_field(cls, self)

class LastRequestField(models.CharField):
    """
    A field that keeps the request that touched an instance
    of a model.
    """
    
    def __init__(self, null=True,  **kwargs):
        super(LastRequestField, self).__init__(null=null,max_length=200, **kwargs)
    
    def contribute_to_class(self, cls, name):
        super(LastRequestField, self).contribute_to_class(cls, name)
        registry = registration.FieldRegistry(self.__class__)
        registry.add_field(cls, self)

class LastIPField(LastRequestField):
    def __init__(self, **kwargs):
        super(LastIPField, self).__init__(**kwargs)

class LastReferrerField(LastRequestField):
    def __init__(self,  **kwargs):
        super(LastReferrerField, self).__init__(**kwargs)

class LastUserAgentField(LastRequestField):
    def __init__(self, **kwargs):
        super(LastUserAgentField, self).__init__(**kwargs)

class LastGetParamsField(LastRequestField):
    def __init__(self, **kwargs):
        super(LastGetParamsField, self).__init__(**kwargs)

class LastPostParamsField(LastRequestField):
    def __init__(self, **kwargs):
        super(LastPostParamsField, self).__init__(**kwargs)

class LastRequestURLField(LastRequestField):
    def __init__(self, **kwargs):
        super(LastRequestURLField, self).__init__(**kwargs)