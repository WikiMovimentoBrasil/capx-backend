from modeltranslation.translator import translator, TranslationOptions
from .models import Organization, OrganizationType


class OrganizationTranslationOptions(TranslationOptions):
    fields = ('organization_name', 'organization_description')


class OrganizationTypeTranslationOptions(TranslationOptions):
    fields = ('type_name', )


translator.register(Organization, OrganizationTranslationOptions)
translator.register(OrganizationType, OrganizationTypeTranslationOptions)