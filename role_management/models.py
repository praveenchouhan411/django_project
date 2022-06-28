from django.db import models
from django.contrib.auth.models import User
from time import time


# Admin Panel Models Here

def get_upload_file_name(instance, filename):
    return "uploaded_file/%s_%s" % (str(time()).replace('.', '_'), filename)


class ModuleList(models.Model):
    # category = models.ForeignKey()
    module_name = models.CharField(max_length=350, unique=True, null=False)
    user_id = models.SmallIntegerField(null=False)
    created_by = models.CharField(max_length=200, null=False)
    date_joined = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.module_name


class UserType(models.Model):
    user_type_name = models.CharField(max_length=350, unique=True, null=False)
    created_by = models.CharField(max_length=200, null=False)
    date_joined = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_type_name


class UserTypeModule(models.Model):
    module_names = models.ForeignKey('ModuleList', on_delete=models.CASCADE, related_name='module_names')
    user_type = models.ForeignKey('UserType', on_delete=models.CASCADE, related_name='user_type')
    module_rights = models.TextField(null=False)

    def __str__(self):
        return self.module_rights


class CustomUserCreation(User):
    # module_name = models.ForeignKey(UserType, on_delete=models.CASCADE, default='')
    user_type = models.ForeignKey('UserType', on_delete=models.CASCADE)
    created_by = models.CharField(max_length=200, null=True)


class PurchaseManager(models.Model):
    full_name = models.CharField(max_length=200, unique=True)
    contact_number = models.CharField(max_length=200, unique=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.FileField(upload_to=get_upload_file_name)
    likes_chesse = models.BooleanField()

    def __bool__(self):
        return self.likes_chesse


class LoginLog(models.Model):
    email_id = models.CharField(max_length=200, unique=True)
    ip_address = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(unique=True)
    loggedin_by = models.IntegerField(null=True)
    loggedin_at = models.DateTimeField(null=True)

    def __int__(self):
        return self.id

# class ABSUser(models.Model):
#    first_name = models.CharField(max_length=255)
#
#    def get_username(self):
#        return self.username
#
#    class Meta:
#        abstract = True
#
#
# class Employee(ABSUser):
#    title = models.CharField(max_length=255)
#
# class EmployeeInfo(Employee):
#    age = models.CharField(max_length=255)

#
#
# class EmployeeUser(object):
#    fname = models.CharField(max_length=255)
#
#    def get_username(self):
#        return self.fname
#

# class EmpUser(object):
#    first_name = models.CharField(max_length=255)
#
#    def get_username(self):
#        return self.username
#
#
# class EmployeeUserInfo(EmpUser, models.Model):
#    department = models.CharField(max_length=255)


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])