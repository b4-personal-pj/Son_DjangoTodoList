# 회원 가입 CBV를 만드는 절차
# status(상태코드) APIView, Response, serializer,user model import
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializer import UserSerializer,ReadUserSerializer,ComtomTokenObtainPairSerializer
from .models import User
from django.contrib import auth
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


# 회원가입
class SignUp(APIView):
    def post(self,request):
        # 데이터 직렬화
        serializer = UserSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid():
            serializer.save()
            # 직렬화 데이터 추출 : https://stackoverflow.com/questions/47714516/how-to-get-field-value-in-the-serializer
            user_name = serializer.validated_data.get('name')
            return Response({'message':f'{user_name}님 환영합니다.'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    # 회원 정보 읽기
    def get(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        serializer = ReadUserSerializer(owner)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # 로그 아웃
    # 로그아웃 기능을 black list로 구현하면 안된다.
    # 나의 생각 정리 : https://velog.io/@rumor/DRF-Simple-JWT-%EB%B8%94%EB%9E%99%EB%A6%AC%EC%8A%A4%ED%8A%B8
    # 요약 : token 인증 방식의 장점인 stateless가 무뎌질 수 있을 것 같다.
    #       블랙리스트 기능은, 관리자가 특정한 token을 차단하는것이 더 바람직 하지 않을까?
    def post(self, request,user_id):
        owner = get_object_or_404(User,id=user_id)
        if request.user == owner:
            token = RefreshToken(request.data.get('refresh'))
            print(token)
            token.blacklist()
            return Response({"message":"로그아웃 하셨습니다."},status=status.HTTP_200_OK)
        else:
            return Response({"message":"잘못된 접근입니다."},status=status.HTTP_400_BAD_REQUEST)

    # 회원 정보 수정
    def put(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        if request.user == owner:
            serializer = UserSerializer(owner,data=request.data,partial=True)
            # partial=True : 부분 업데이트
            if serializer.is_valid():
                serializer.save()
                # 회원 정보 수정후, 필요한 값만 추출하여 발송
                update_user_info = ReadUserSerializer(owner)
                return Response(update_user_info.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)

    # 회원 정보 삭제
    def delete(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        if request.user == owner:
            owner.delete()
            return Response({"message":"회원 탈퇴 하셨습니다."},status=status.HTTP_200_OK)
        else:
            return Response({"error":"권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = ComtomTokenObtainPairSerializer