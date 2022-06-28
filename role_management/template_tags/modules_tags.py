from django import template
from ..models import ModuleList, CustomUserCreation, UserTypeModule

register = template.Library()


@register.simple_tag
def getgenre():
    """ Get Module for user basis """

    module_names = []

    modules = ModuleList.objects.filter(is_active=True).order_by('id').all()

    for module in modules:
        module = str(module).title().replace('_', ' ')
        print("module name>>>>>>>>>>>>>>>>", module)
        module_names.append(module)

    return module_names
