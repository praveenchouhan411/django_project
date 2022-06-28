from .models import ModuleList, CustomUserCreation, UserTypeModule


def get_modules(request):
    """ GET Activate Modules for Sidebar """

    try:
        module_names = []
        context_data = dict()
        user_id = request.user.id

        print("id", user_id)
        print("issuperuser", request.user.is_superuser)

        if request.user.is_superuser:
            module_list = ModuleList.objects.filter(is_active=True).all()

            for module in module_list:
                module_names.append({str(module.module_name).replace('_', ' ').title(): str(module.module_name).replace(
                    '_', ' ').title()})

        elif user_id is None:
            return context_data
        else:
            user_type_id = CustomUserCreation.objects.values_list('user_type_id', flat=True).get(user_ptr_id=user_id,
                                                                                                 is_active=True)

            user_modules = UserTypeModule.objects.values_list('module_names_id', flat=True).filter(
                user_type_id=user_type_id)

            for module_id in user_modules:
                module_name = ModuleList.objects.values_list('module_name', flat=True).filter(id=module_id,
                                                                                              is_active=True).order_by(
                    'id').all()

                if module_name:
                    module_names.append(
                        {str(module_name[0]).replace('_', ' ').title(): str(module_name[0]).replace('_', ' ').title()})

        context_data['module_list'] = module_names

        return context_data

    except Exception as e:
        print("Exception E:", e)
        return context_data


def get_available_modules(request):
    """ get available module """

    try:
        module_names = []
        context_data = dict()
        user_id = request.user.id

        print("id", user_id)
        print("issuperuser", request.user.is_superuser)

        if request.user.is_superuser:
            module_list = ModuleList.objects.filter(is_active=True).all()

            for module in module_list:
                module_names.append({str(module.module_name).replace('_', ' ').title(): str(module.module_name).replace(
                    '_', ' ').title()})

        elif user_id is None:
            return context_data
        else:
            user_type_id = CustomUserCreation.objects.values_list('user_type_id', flat=True).get(user_ptr_id=user_id,
                                                                                                 is_active=True)
            if user_type_id:

                user_modules = UserTypeModule.objects.values_list('module_names_id', flat=True).filter(
                    user_type_id=user_type_id)

                for module_id in user_modules:
                    module_name = ModuleList.objects.values_list('module_name', flat=True).filter(id=module_id,
                                                                                                  is_active=True).order_by(
                        'id').all()

                    if module_name:
                        module_names.append(
                            {str(module_name[0]).replace('_', ' ').title(): str(module_name[0]).replace('_', ' ').title()})

        context_data['module_list'] = module_names

        return context_data

    except Exception as e:
        print("Exception E:", e)
        return context_data
