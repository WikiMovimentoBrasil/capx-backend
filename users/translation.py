from modeltranslation.translator import translator, TranslationOptions
from .models import OrganizationType


class OrganizationTypeTranslationOptions(TranslationOptions):
    fields = ('type_name', )


translator.register(OrganizationType, OrganizationTypeTranslationOptions)