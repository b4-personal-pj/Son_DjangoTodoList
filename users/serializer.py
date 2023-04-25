# serialzier model을 만드는 단계
# 1. serializer , app model import
# 2. serializer class 생성 및 , serializer model 상속
# 3. 연결할 app model 및 fields 정의
# 4. 회원가입시 비밀번호 복호화 과정 필요

from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    # 회원 가입, 오버라이딩
    def create(self, validated_data):
        # 부모 클래스 호출, 인스턴스 반환
        user = super().create(validated_data)
        # 비밀번호 복호화
        user.set_password(user.password)
        user.save()
        return user



    # 회원 정보 수정, 오버라이딩
    def update(self, instance, validated_data):
        user = super().update(instance,validated_data)
        # 비밀번호 복호화
        user.set_password(user.password)
        user.save()
        return user

class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name','email', 'gender', 'introduction','age')

class ComtomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['name'] = user.name
        token['gender'] = user.gender
        token['age'] = user.age

        return token