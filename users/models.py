from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# ,'name','gender','introduction'
class UserManager(BaseUserManager):
    def create_user(self, email, name,age, gender, introduction, password=None):
        gender = gender.upper()

        if not email:
            raise ValueError('사용자 이메일은 필수 기입 사항입니다.')

        elif not name:
            raise ValueError('사용자 이름은 필수 기입 사항입니다.')

        elif not gender:
            raise ValueError('사용자의 성별은 필수 선택 사항입니다.')

        elif not gender == 'M' or gender == 'F':
            raise ValueError('올바른 성별을 입력해주세요 M/F')

        elif not age:
            raise ValueError('사용자의 나이를 입력해주세요.')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            gender=gender,
            introduction=introduction,
            age=age,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, gender, introduction,age, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            gender=gender,
            introduction=introduction,
            age=age,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    GENDER_CHOICES = (
        ('M', '남성'),
        ('F', '여성'),
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    age = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    introduction = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'gender', 'introduction','age']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
