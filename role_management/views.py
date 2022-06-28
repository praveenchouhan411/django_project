import json
from _operator import itemgetter
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf
from django.utils import timezone
from .forms import ModuleListForm
from .models import ModuleList, UserTypeModule, UserType, CustomUserCreation
from .forms import AdminRegistrationForm
from django.contrib.auth.models import User
from django.views import View
import logging
from .modules import get_modules
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from django.template.response import TemplateResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework import mixins, generics

logger = logging.getLogger(__name__)


def get_module_list():
    """ GET List of Module in Application """

    try:
        modules = settings.INSTALLED_APPS
        module_dict = {}

        module_name_list = [module.split('.')[2] for module in modules if module.startswith('project_apps.module_apps')]

        for module in module_name_list:
            module_name = module.replace('_', ' ')
            module_dict[module] = module_name

        return module_dict

    except Exception as e:
        print("Exception E: ", e)
        return None


def module_exist(module_name):
    """ Module exist or not """

    try:
        module_name = str(module_name).replace('_', ' ').title()
        module = ModuleList.objects.filter(module_name=module_name).all()

    except Exception as e:
        print("Exception E: ", e)
        return None

    return module


@login_required
def create_module(request):
    try:
        args = {}

        if request.POST:
            form = ModuleListForm(request.POST)
            module_name = request.POST.get('module_name')

            is_module_exist = module_exist(module_name)

            if form.is_valid() and not is_module_exist:
                module = form.cleaned_data['module_name'].replace('_', ' ').title()
                module = ModuleList.objects.create(module_name=module, user_id=request.user.id,
                                                   created_by=request.user.username)
                module.save()
                return HttpResponseRedirect('/management/module/get/')
            else:
                return HttpResponseRedirect('/management/module/add/')

        else:
            modules = get_module_list()
            args['modules'] = modules
            form = ModuleListForm()

        args['form'] = form
        args['host'] = request.META['HTTP_HOST'] + '/admin/invalid_login/'

        return render(request, 'create_module.html', args)

    except Exception as e:
        print("Exception E: ", e)
        return render(request, 'create_module.html', args)


class ModuleListView(View):
    """ ModuleList  """

    modules = {}

    # @login_required()
    def get(self, request):

        try:
            if request.user.is_superuser:
                zip_modules = self.get_modules()

                zip_module_name = zip_modules['module_list']
                zip_module_list = zip_modules['modules']

                print("zpi module name", zip_module_name)
                print("zpi module name", zip_module_list)

                self.modules['modules'] = zip(zip_module_name, zip_module_list)

            else:
                return HttpResponse("Permission Denied")

            return render(request, 'module_list.html', self.modules)

        except Exception as e:
            print("Exception E: ", e)
            return render(request, 'module_list.html', self.modules)

    # @login_required()
    def post(self, request):

        try:
            module_id = request.POST['module_id']
            module_name = request.POST['module_name']
            is_active = request.POST['is_active']

            ModuleList.objects.filter(id=module_id).update(module_name=module_name,
                                                           is_active=True if is_active == 'True' else False)

            self.modules['modules'] = self.get_modules()

            return render(request, 'module_list.html', self.modules)

        except Exception as e:
            print("Exception E: ", e)
            return render(request, 'module_list.html', self.modules)

    @staticmethod
    def get_modules(self):
        """ GET List of Activated Modules """

        try:
            print("get moduele inside")
            modules = []
            module_obj = ModuleList.objects.all()

            for module in module_obj:
                modules.append(str(module).replace('_', ' ').title())

            list_length_module = len(module_obj)
            print(list_length_module)

            # list_length_module = [i for i in range(1, list_length_module + 1)]

            module_details = {
                'module_list': module_obj,
                'modules': modules
            }

            return module_details

        except Exception as e:
            print("Exception E: ", e)


@login_required
def profile(request):
    """ Admin Profile Page """

    try:
        users = {}

        if request.method == 'POST':
            user_name = request.POST['user_name']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            # password = request.POST['password']
            email = request.POST['email']

            User.objects.filter(id=request.user.id).update(username=user_name, first_name=first_name,
                                                           last_name=last_name,
                                                           email=email)

            # u = User.objects.get(username__exact=user_name)
            # u.set_password(password)
            # u.save()

            return HttpResponseRedirect('/management/profile')

            # users['users'] = users_obj

        # users.update(csrf(request))

        users_obj = User.objects.get(id=request.user.id)

        users['users'] = users_obj

        return render(request, 'profile.html', users)

    except Exception as e:
        print("Exception E: ", e)
        return render(request, 'profile.html', users)


@login_required
def create_user(request):
    """ Create Customers Account """

    try:
        args = {}

        if request.method == 'POST':
            form = AdminRegistrationForm(request.POST)

            if form.is_valid():
                print("form: ", args)

                form.save()
                return HttpResponseRedirect('/management/admin/user_list')


        args.update(csrf(request))
        obj = AdminRegistrationForm()

        user_type = UserType.objects.all()

        if len(user_type) is 0:
            args['user_type'] = False
        else:
            args['user_type'] = True

        args['form'] = obj

        print("obj: ", obj)
        return render(request, 'create_user.html', args)

    except Exception as e:
        print("Exception E: ", e)
        return render(request, 'create_user.html', args)


@login_required
def user_list(request):
    """ Get Users/Customers Account """

    try:
        users = {}

        if request.POST:
            user_id = request.POST['user_id']
            username = request.POST['username']
            updated_user_type = request.POST['type']
            is_active = request.POST['is_active']
            email = request.POST['email']

            CustomUserCreation.objects.filter(id=int(user_id)).update(username=username, email=email,
                                                                      is_active=True if is_active == 'True' else False)

            user_type_name = UserType.objects.get(user_type_name=updated_user_type)
            CustomUserCreation.objects.filter(id=int(user_id)).update(user_type=user_type_name)

        if request.method == 'GET':
            if not request.user.is_superuser:
                return HttpResponse('Permission Denied')

        users_obj = CustomUserCreation.objects.all()

        print("users_obj: ", users_obj)

        for u in users_obj:
            print("Users list", users['users'])
            print("usrs", u)

        list_length_users = len(users_obj)

        list_length_module = [i for i in range(1, list_length_users + 1)]
        users['users'] = zip(users_obj, list_length_module)

        return render(request, 'user_list.html', users)

    except Exception as e:
        print("Exception E: ", e)
        return render(request, 'user_list.html', users)


@login_required
def create_user_type(request):
    """ Get Users/Customers Account """

    try:
        modules_dict = {}
        modules = []

        if request.GET:
            modules_dict['host'] = request.META['HTTP_HOST']

        if request.POST:
            rights_length = 0

            user_type = request.POST['user_type']

            user_type_name = UserType.objects.filter(user_type_name__iexact=user_type)

            if not user_type_name:

                form_data = dict(request.POST)

                all_rights = ['create', 'read', 'edit', 'delete']

                store_user_type = UserType.objects.create(user_type_name=user_type, date_joined=timezone.now(),
                                                          created_by=request.user.username)
                store_user_type.save()
                user_type_id = store_user_type.id

                for key in form_data:
                    if key not in ['csrfmiddlewaretoken', 'user_type']:

                        user_rights = form_data[key]

                        user_rights_dict = {}

                        store_user_rights = [
                            user_rights_dict.update(
                                {rights: 'true'}) if rights in user_rights else user_rights_dict.update(
                                {rights: 'false'}) for rights in
                            all_rights]

                        rights_list = []

                        store_user_rights = [(k, user_rights_dict[k],) for k in sorted(user_rights_dict)]

                        for rights in store_user_rights:
                            rights_length = rights_length + 1
                            rights_list.append((rights, rights_length))

                        user_type_creation = UserTypeModule.objects.create(module_rights=rights_list,
                                                                           module_names_id=int(key),
                                                                           user_type_id=user_type_id)

                        user_type_creation.save()
                        rights_given = True

                    else:
                        rights_given = False

                # if rights_given is False:
                #     print("right is given:", rights_given)
                #
                #     module_list = ModuleList.objects.filter(is_active=True).all()
                #
                #     store_user_rights = [(('create', 'false'), 1), (('delete', 'false'), 2),
                #                          (('edit', 'false'), 3),
                #                          (('read', 'false'), 4)]
                #
                #     for module in module_list:
                #         user_type_creation = UserTypeModule.objects.create(module_rights=store_user_rights,
                #                                                            module_names_id=module.id,
                #                                                            user_type_id=user_type_id)
                #
                #         user_type_creation.save()

                return HttpResponseRedirect('/management/admin/get_users_type')

        if request.method == 'GET':
            if not request.user.is_superuser:
                return HttpResponse('Permission Denied')

        module_list = ModuleList.objects.filter(is_active=True).all()

        for module in module_list:
            modules.append(str(module).replace('_', ' ').title())

        list_length_users = len(module_list)

        if list_length_users is 0:
            modules_dict['activate_module_avail'] = False
        else:
            modules_dict['activate_module_avail'] = True
            list_length_module = [module_list.id for module_list in module_list]
            serial_numbers = [i for i in range(1, list_length_users + 1)]

            modules_dict['modules'] = zip(modules, list_length_module, serial_numbers)

        return render(request, 'create_user_type.html', modules_dict)

    except Exception as e:
        print("Exception E: ", e)
        return render(request, 'create_user_type.html', modules_dict)


@login_required
def user_type_list(request):
    """ Get Users/Customers Account """

    try:
        if request.POST:

            modules_id = set()
            result_rights_list = []
            user_type_id = request.POST.get('user_type_id')
            user_type_name = request.POST.get('user_type_name')
            is_active = request.POST.get('is_active')
            user_type_details_dict = dict(request.POST)

            UserType.objects.filter(id=user_type_id).update(user_type_name=user_type_name, is_active=is_active)

            for user_type_right_info in user_type_details_dict:

                if user_type_right_info.startswith('checkbox_'):
                    token_list = user_type_right_info.split('_')
                    module_id = int(token_list[1])
                    modules_id.add(module_id)
                    result_rights_list.append(
                        ((token_list[2], user_type_details_dict[user_type_right_info][0]), int(token_list[3])))

                    result_rights_list.sort(key=lambda tup: tup[1])
                    del user_type_right_info

            for module in modules_id:
                md_id = module
                md_rights = result_rights_list[:4]
                del result_rights_list[:4]
                UserTypeModule.objects.filter(module_names_id=md_id, user_type_id=user_type_id).delete()

                user_type_creation = UserTypeModule.objects.create(module_rights=md_rights,
                                                                   module_names_id=md_id,
                                                                   user_type_id=user_type_id)

                user_type_creation.save()

            return HttpResponseRedirect('/management/admin/get_users_type')

        if request.method == 'GET':
            if not request.user.is_superuser:
                return HttpResponse('Permission Denied')

        users_type = {}
        user_type_list = UserType.objects.all()

        list_length_users = len(user_type_list)
        list_length_module = [i for i in range(1, list_length_users + 1)]

        users_type['user_type_list'] = zip(user_type_list, list_length_module)

        return render(request, 'user_type_list.html', users_type)

    except Exception as e:
        print("Exception E: ", e)
        return render(request, 'user_type_list.html', users_type)


@login_required
def edit_module(request):
    """ Admin Profile Page """

    try:
        if request.method == 'GET':
            if not request.user.is_superuser:
                return HttpResponse('Permission Denied')

        modules = {}
        module_id = request.GET['module_id']
        module_details = ModuleList.objects.filter(id=module_id).all()

        module_details.module_name = str(module_details[0].module_name).replace('_', ' ').title()
        modules['module_details'] = module_details

        return render(request, 'edit_module.html', modules)

    except Exception as e:
        print("Exception E: ", e)
        return render(request, 'edit_module.html', modules)


@login_required
def edit_user(request):
    """ Admin Profile Page """

    try:
        if request.method == 'GET':
            if not request.user.is_superuser:
                return HttpResponse('Permission Denied')

        users = {}
        user_id = request.GET['user_id']
        users_details = CustomUserCreation.objects.filter(id=user_id).all()

        for user_detail in users_details:
            user_id = user_detail.id
            user_name = user_detail.username
            user_type_id = user_detail.user_type_id
            is_active = user_detail.is_active
            password = user_detail.password
            email = user_detail.email
            user_created_by = user_detail.created_by

        users_type_name = UserType.objects.values_list('user_type_name', flat=True).filter(id=user_type_id)[0]
        users_type_list = UserType.objects.values_list('user_type_name').all()

        users['user_id'] = user_id
        users['user_name'] = user_name
        users['user_type_id'] = user_type_id
        users['user_created_by'] = user_created_by
        users['users_type_name'] = users_type_name
        users['is_active'] = is_active
        users['password'] = password
        users['email'] = email
        users['users_type_list'] = users_type_list

        # users['users'] = users_details

        return render(request, 'edit_user.html', users)

    except Exception as e:
        print("Exception E: ", e)
        return render(request, 'edit_user.html', users)


@login_required
def edit_user_type(request):
    """ Edit UserType Form """

    try:
        if request.method == 'GET':
            if not request.user.is_superuser:
                return HttpResponse('Permission Denied')

        user_type_details = {}
        module_name_list = []
        sorted_module_list = []
        user_type_module_id = []
        module_ids = []
        max_right = 0

        module_name_id = None
        user_type_id = int(request.GET['user_type_id'])

        user_type_list = UserType.objects.get(id=user_type_id)

        modules = ModuleList.objects.filter(is_active=True)

        for mod_id in modules:
            module_ids.append(mod_id.id)

        print("module_ids", module_ids)

        user_type_modules_details = UserTypeModule.objects.filter(user_type_id=user_type_id)

        print("user_type_module", user_type_modules_details)

        if user_type_modules_details:
            for user_type_module in user_type_modules_details:
                module_name_id = user_type_module.module_names_id
                user_type_module_id.append(module_name_id)

                module_details = ModuleList.objects.get(id=module_name_id)

                module_name_list.append({'module_id': module_name_id, 'module_name': module_details.module_name,
                                         'module_rights': eval(user_type_module.module_rights)})

                sorted_module_list = sorted(module_name_list, key=itemgetter('module_id'))

            no_of_modules = len(sorted_module_list) - 1

            max_right = module_name_list[no_of_modules]['module_rights'][3][1]

        ids = [mod_id for mod_id in module_ids if mod_id not in user_type_module_id]

        for id in ids:
            print("id: ", id)

            new_module_rights = [(('create', 'false'), (max_right + 1)), (('delete', 'false'), (max_right + 2)),
                                 (('edit', 'false'), (max_right + 3)), (('read', 'false'), (max_right + 4))]

            max_right = new_module_rights[3][1]

            module_name = ModuleList.objects.values_list('module_name', flat=True).filter(id=id)

            sorted_module_list.append({'module_id': id, 'module_name': module_name[0],
                                       'module_rights': new_module_rights})

        user_type_details['user_type_details'] = user_type_list
        user_type_details['user_type_id'] = user_type_id
        user_type_details['module_name_list'] = sorted_module_list
        user_type_details['module_id'] = module_name_id

        return render(request, 'edit_user_type.html', user_type_details)

    except Exception as e:
        print("Exception E: ", e)
        return render(request, 'edit_user_type.html', user_type_details)


@login_required
def delete_module(request):
    """ Delete Module """

    try:
        if request.method == 'GET':

            if not request.user.is_superuser:
                return HttpResponse('Permission Denied')

            module_id = int(request.GET['module_id'])

            delete_module = get_object_or_404(ModuleList, id=module_id)
            delete_module.delete()

        return HttpResponseRedirect('/management/module/get/')

    except Exception as e:
        print("Exception E: ", e)
        return HttpResponseRedirect('/management/module/get/')


@login_required
def delete_user(request):
    """ Delete Module """

    try:
        if request.method == 'GET':

            if request.method == 'GET':
                if not request.user.is_superuser:
                    return HttpResponse('Permission Denied')

            user_id = int(request.GET['user_id'])
            obj = get_object_or_404(User, id=user_id)
            obj.delete()

        return HttpResponseRedirect('/management/admin/user_list/')

    except Exception as e:
        print("Exception E: ", e)
        return HttpResponseRedirect('/management/admin/user_list/')


@login_required
def delete_user_type(request):
    """ Delete Module """

    try:
        if request.method == 'GET':

            if request.method == 'GET':
                if not request.user.is_superuser:
                    return HttpResponse('Permission Denied')

            user_type_id = int(request.GET['user_type_id'])

            delete_user_type_id = get_object_or_404(UserType, id=user_type_id)
            delete_user_type_id.delete()

        return HttpResponseRedirect('/management/admin/get_users_type/')

    except Exception as e:
        print("Exception E: ", e)
        return HttpResponseRedirect('/management/admin/get_users_type/')


class Dashboard(generics.GenericAPIView, mixins.ListModelMixin):
    """ ModuleList  """

    modules = {}
    permission_classes = [AllowAny]

    def get(self, request):
        # print("format: ", self.request.accepted_renderer.format)
        # print("request.user.is_authenticated:", request.user.is_authenticated)

        if self.request.accepted_renderer.format is 'api':

            request.user.id = int(request.session['id'])
            request.user.is_superuser = request.session['is_superuser']
            mod = get_modules(request)

            return render(request, 'users_dashboard.html',
                          {'super_user': request.user.is_superuser, 'mod_list': mod})

        else:
            mod = get_modules(request)
            return Response(mod, status=HTTP_200_OK)
