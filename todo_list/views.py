from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

# Create your views here.

class PostView(APIView):
    # 모든 포스트 조회 (제목,작성자만 출력)
    def get(self,request):
        pass
    # 게시글 작성
    def post(self,request):
        pass

class DetailPostView(APIView):
    # 게시글 상세 조회 (제목,작성자,내용,작성시간,수정시간)
    def get(self,request,post_id):
        pass

    # 게시글 수정
    def put(self,request,post_id):
        pass

    # 게시글 삭제
    def delete(self, request, post_id):
        pass

