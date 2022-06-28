from .models import ModuleList, UserType, UserTypeModule
from .models import CustomUserCreation, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm


class ModuleListForm(forms.ModelForm):
    # name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super(ModuleListForm, self).__init__(*args, **kwargs)
        # self.fields['created_by'] = forms.ModelChoiceField(
        #     queryset=User.objects.filter(is_superuser=True), initial=''
        # )
        self.fields['module_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Module Name'})
        self.fields['user_id'].widget.attrs.update({'class': 'form-control', 'readonly': True})
        self.fields['created_by'].widget.attrs.update({'class': 'form-control', 'readonly': True})

    class Meta:
        model = ModuleList
        fields = '__all__'
        exclude = ('is_active','date_joined')


class AdminRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # module_name = forms.ChoiceField
    # user_type = forms.ChoiceField(choices=['is_superuser', 'is_staff'])

    class Meta:
        model = CustomUserCreation
        fields = ('user_type', 'username', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'created_by')

    def __init__(self, *args, **kwargs):
        super(AdminRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].empty_label = 'Select User Type'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.user_type(self.cleaned_data["user_type"])
        user.email = self.cleaned_data['email']
        # user.is_superuser = self.cleaned_data['is_superuser']
        user.is_staff = True
        user.is_active = True

        if commit:
            user.save()

        return user


# class UserTypeForm(forms.ModelForm):
#
#     class Meta:
#         model = UserType
#         fields = ('user_type_name', )
#
#     def save(self, commit=True):
#         user_type_name = super(forms.ModelForm, self).save(commit=False)
#         user_type_name.name = self.cleaned_data['user_type_name']
#
#         # Check to see if any users already exist with this email as a username.
#         try:
#             match = UserType.objects.get(user_type_name=user_type_name.name)
#         except UserType.DoesNotExist:
#             # Unable to find a user, this is fine
#             if commit:
#                 user_type_name.save()
#
#             return user_type_name
#
#         # A user was found with this as a username, raise an error.
#         raise forms.ValidationError('user_type_name is already in use.')


# class UserTypeModuleForm(forms.ModelForm):
#
#     class Meta:
#         model = UserTypeModule
#         exclude = ('module_type_id',)


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = ('likes_chesse', )
