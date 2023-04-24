# 회원 가입 CBV를 만드는 절차
# status(상태코드) APIView, Response, serializer,user model import
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import UserSerializer
from .models import User


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

