from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from .models import Post
from .serializer import PostSerializer,DetailPostSerializer,CreatePostSerializer
from django.contrib import auth


class PostView(APIView):
    # 모든 포스트 조회 (제목,작성자만 출력)
    def get(self,request):
        post = Post.objects.all()
        serialzier = PostSerializer(post,many=True)
        return Response(serialzier.data,status=status.HTTP_200_OK)
    # 게시글 작성
    def post(self,request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인이 필요합니다."},status=status.HTTP_401_UNAUTHORIZED)
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DetailPostView(APIView):
    # 게시글 상세 조회 (제목,작성자,내용,작성시간,수정시간)
    def get(self,request,post_id):
        post = get_object_or_404(Post,id=post_id)
        serializer = DetailPostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # 게시글 수정
    def put(self,request,post_id):
        post = get_object_or_404(Post,id=post_id)
        if not request.user == post.owner:
            return Response("권한이 없습니다.",status=status.HTTP_400_BAD_REQUEST)

        serializer = CreatePostSerializer(post,data=request.data)
        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    # 게시글 삭제
    def delete(self, request, post_id):
        post = get_object_or_404(Post,id=post_id)

        if not request.user == post.owner:
            return Response({"error":"권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)

        post.delete()
        return Response({"message":"게시글을 삭제했습니다."},status=status.HTTP_200_OK)


