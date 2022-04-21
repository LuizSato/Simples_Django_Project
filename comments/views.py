from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CommentSerializer
from .models import Comment

from rest_framework import generics, permissions, serializers


from .utils import serializer_multiples

class Get_Comment(APIView):
    def get(self, request, format=None):
        comments_instance = Comment.objects.all()
        comments_serialized = serializer_multiples(CommentSerializer, comments_instance)
        return Response(status=status.HTTP_200_OK, data=comments_serialized)

class Get_User_Comments(APIView):
    def get(self, request, user_id, format=None):
        comments_instance = Comment.objects.filter(user_id=user_id)
        comments_serialized = serializer_multiples(CommentSerializer, comments_instance)
        return Response(status=status.HTTP_200_OK, data=comments_serialized)

class Get_Comment_Thread(APIView):
    def get(self, request, comment_id, format=None):
        main_thread = Comment.objects.filter(id=comment_id)
        following_threads = Comment.objects.filter(parent_comment=comment_id).order_by('timestamp')

        main_thread_serialized = serializer_multiples(CommentSerializer, main_thread)
        following_threads_serialized = serializer_multiples(CommentSerializer, following_threads)

        main_thread_serialized.append(following_threads_serialized)
        return Response(status=status.HTTP_200_OK, data=main_thread_serialized)



class Save_Comment(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        try:
            request_body = request.data
            comment_serialized = CommentSerializer(data=request_body)
            if comment_serialized.is_valid():
                comment_serialized.save()
            else:
                raise Exception(
                    'Something went wrong, please try again later.'
                )
            if 'parent_comment' in request_body:
                    response_body = 'Reply Sent'
            else: 
                response_body = 'Comment Sent'
            return Response(status=status.HTTP_201_CREATED, data=response_body)
        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(err))


class Update_Comment(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        try:
            request_body = request.data
            try:
                comment_instance = Comment.objects.get(id=request_body['id'])
                comment_updated_serializer = CommentSerializer(comment_instance, data={'text_body': request_body['text_body']}, partial=True)
                if comment_updated_serializer.is_valid():
                    comment_updated_serializer.save()
                else: 
                    raise Exception(
                        'Something went wrong updating the comment, please try again later.'
                    )
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Comment.DoesNotExist as err:
                return Response(status=status.HTTP_404_NOT_FOUND, data=str(err))
        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(err))

class Delete_Comment(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, format=None):
        try:
            request_body = request.data
            comment_instance = Comment.objects.filter(id=request_body['comment_id'], user_id=request_body['user_id'])

            if comment_instance.exists():
                comment_instance.delete()
            else:
                raise Exception(
                    'Could not delete this comment at this time, please try again later'
                )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as err:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=str(err))
