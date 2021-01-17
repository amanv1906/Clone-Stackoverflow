from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from stackoverflow.helper import (attach_profile, calculate_score,
                                  delete_vote_object, went_wrong)
from stackoverflow.models import Question, Tag, Answer, Vote, Comment
from django.db.models import Count, F
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from stackoverflow.serializers import (SignupSerializer,
                                       AuthenticateSerializer,
                                       UserInfoSerializer,
                                       QuestionSerializer,
                                       QuestionPostSerializer,
                                       TagSerializer,
                                       AnswerPostSerializer,
                                       CommentPostSerializer)


class Signup(APIView):
    '''Api for signup view connect it to /signup'''

    def post(self, request):
        '''method for handeling post requests'''

        # passed recieved data to serializer
        signup_serializer = \
            SignupSerializer(data=request.data)
        signup_serializer.is_valid(raise_exception=True)

        # signup_serializer will create user and return
        # toke serializer(required format of json for react)
        token_serializer = signup_serializer.save()
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data)


class Authenticate(ObtainAuthToken):
    '''Api view for autheticate of login'''

    def post(self, request):
        '''method for handeling post requests'''
        authenticate_serializer =\
            AuthenticateSerializer(data=request.data)
        authenticate_serializer.is_valid(raise_exception=True)

        # authenticate_serializer will validate data and return
        # toke serializer(required format of json for react)
        token_serializer = authenticate_serializer.validated_data
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data)


class ListUser(APIView):
    '''Api view for list all users'''

    def get(self, request):
        '''method for handeling get request'''

        # querying users and pass to attach profile
        users = attach_profile(User.objects)
        # serializing data
        user_info_serializer =\
            UserInfoSerializer(users, many=True)
        return Response(user_info_serializer.data)


class UserSearch(APIView):
    '''Api view for user searching'''

    def get(self, request, username):
        '''method to handle get requests'''

        # querying users and attach profile to convert required format
        users = attach_profile(
            User.objects.filter(username__icontains=username)
        )

        # serializing data
        user_info_serializer =\
            UserInfoSerializer(users, many=True)
        return Response(user_info_serializer.data)


class UserDetail(APIView):
    '''Api view for user details'''

    def get(self, request, username):
        '''method for handeling get requests'''

        user = attach_profile(
            User.objects.filter(username=username)
        )
        if not user:
            message = {
                'message': 'user not found'
            }
            return Response(message, status.HTTP_404_NOT_FOUND)
        user = user[0]
        user_info_serializer = UserInfoSerializer(user)
        return Response(user_info_serializer.data)


class QuestionView(generics.ListCreateAPIView):
    '''
    API for listing out all
        the questions
    '''

    queryset = Question.objects.all()
    # show all the questions asked by users

    serializer_class = QuestionSerializer


class QuestionDetailView(APIView):
    '''
    Gives the detail of particular
    question
    '''

    def get(self, request, q_id):
        '''
        handle get request
        '''
        # if my question does not exist
        try:
            Question.objects.get(pk=q_id)
        except Question.DoesNotExist:
            msg = {"message": "Question doesn't exist"}
            return Response(msg, status=404)

        query = Question.objects.all().filter(id=q_id).first()
        query.views = query.views + 1

        # whenever question clicked view count increases
        query.save()
        serial = QuestionSerializer(query)
        return Response(serial.data)

    def delete(self, request, q_id):
        '''
        to delete the question
        with particular id
        '''

        instance = Question.objects.get(id=q_id)
        instance.delete()
        return Response(status=201)


class QuestionTag(APIView):
    '''
    give the questions
    of the selected tags
    '''

    def get(self, request, tag):
        query = Question.objects.filter(tags__name=tag)

        serializer = QuestionSerializer(query, many=True)
        return Response(serializer.data)


class UserQuestion(APIView):
    '''
    give the questions
    asked by user
    '''

    def get(self, request, name):
        query = Question.objects.filter(author__username=name)

        serializer = QuestionSerializer(query, many=True)
        return Response(serializer.data)


class QuestionPost(APIView):
    '''
    Post the question
    with particular tag
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.data['author'] = request.user.id
        # passing the data to serializer for overriding create

        serializer = QuestionPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(serializer.errors)


class PopularTags(APIView):
    '''
    API for printing popular tags
    '''

    def get(self, request):
        query = Question.objects.values('tags__name')\
            .annotate(count=Count('tags__name'))\
            .order_by('-count')[:20]

        # i want only top 20 as my popular tags
        serial = TagSerializer(query, many=True)
        return Response(serial.data)


class TagsView(APIView):
    '''
    API for showing all the
    '''

    def get(self, request):
        query = Question.objects.values('tags__name')\
            .annotate(count=Count('tags__name'))\
            .order_by('-count')

        # for showing all the tags
        serial = TagSerializer(query, many=True)
        return Response(serial.data)


class TagSearchView(APIView):
    '''
    For searching the tags
    '''
    def get(self, request, tag):
        query = Tag.objects.values('name')\
            .filter(name__icontains=tag)\
            .annotate(count=Count('question__id'),
                      tags__name=F('name')
                      )
        serialize = TagSerializer(query, many=True)
        return Response(serialize.data)


class AnswerView(APIView):
    '''
    API View for post answer and delete answer
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        request.data['author'] = request.user.id
        request.data['question'] = question_id
        serializer = AnswerPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Question.objects.filter(id=question_id).first()
            serializer_data = QuestionSerializer(data)
            return Response(serializer_data.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, question_id, answer_id):
        answer = Answer.objects.filter(id=answer_id).first()
        if answer:
            answer.delete()
            data = Question.objects.filter(id=question_id).first()
            serializer_data = QuestionSerializer(data)
            return Response(serializer_data.data)
        msg = {"meassage": "Answer doesn't exist"}
        return Response(msg, status=404)


class CommentQuestion(APIView):
    '''
     Api view for Post Comment And Delete comment on Question
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        request.data['body'] = request.data['comment']
        request.data['author'] = request.user.id
        request.data['question'] = question_id
        del request.data['comment']
        serializer = CommentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Question.objects.filter(id=question_id).first()
            serializer_data = QuestionSerializer(data)
            return Response(serializer_data.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, question_id, comment_id):
        comment = Comment.objects.filter(id=comment_id).first()
        if comment:
            comment.delete()
            data = Question.objects.filter(id=question_id).first()
            serializer_data = QuestionSerializer(data)
            return Response(serializer_data.data)
        msg = {"message": "message doesn't exist"}
        return Response(msg, status=404)


class CommentAnswer(APIView):
    '''
    Api View for Post comment and Delete Comment on Answer
    '''
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id, answer_id):
        request.data['body'] = request.data['comment']
        request.data['author'] = request.user.id
        request.data['answer'] = answer_id
        del request.data['comment']
        serializer = CommentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = Question.objects.filter(id=question_id).first()
            serializer_data = QuestionSerializer(data)
            return Response(serializer_data.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, question_id, answer_id, comment_id):
        comment = Comment.objects.filter(id=comment_id).first()
        if comment:
            comment.delete()
            data = Question.objects.filter(id=question_id).first()
            serializer_data = QuestionSerializer(data)
            return Response(serializer_data.data)
        msg = {"message": "message doesn't exist"}
        return Response(msg, status=404)


class Upvote(APIView):
    '''Api view to upvote a question or answer'''

    # adding permissions for upvote api
    permission_classes = [IsAuthenticated]

    def get(self, request, question_id, answer_id=None):
        '''method for handle get requests'''

        if answer_id:
            # deleting vote object for answers of loggedin user
            delete_vote_object(request.user, answer_id=answer_id)

            # creating vote object for loggedin used with vote=1
            Vote.objects.create(user=request.user, answer_id=answer_id)

            # calculating new score
            response = calculate_score(answer_id, Answer)
            if response:
                return response
        else:
            # deleting vote objects if there is any
            delete_vote_object(request.user, question_id=question_id)

            # creating vote object for loggedin user with vote=-1
            Vote.objects.create(user=request.user, question_id=question_id)

            # calculating new score
            response = calculate_score(question_id, Question)
            if response:
                return response
        question = Question.objects.filter(id=question_id)
        if not question:
            return Response(
                went_wrong,
                status.HTTP_404_NOT_FOUND
            )
        question = question[0]
        question_serializer = QuestionSerializer(question)
        return Response(question_serializer.data)


class Downvote(APIView):
    '''Api view to upvote a question or answer'''

    # adding permissions for upvote api
    permission_classes = [IsAuthenticated]

    def get(self, request, question_id, answer_id=None):
        '''method for handle get requests'''

        if answer_id:
            # deleting vote object of loggedin user
            delete_vote_object(request.user, answer_id=answer_id)

            # creating vote object for loggedin used with vote=1
            Vote.objects.create(
                user=request.user,
                answer_id=answer_id,
                vote=-1
            )

            # calculating new score
            response = calculate_score(answer_id, Answer)
            if response:
                return response
        else:
            # deleting vote objects if there is any
            delete_vote_object(request.user, question_id=question_id)

            # creating vote object for loggedin user with vote=-1
            Vote.objects.create(
                user=request.user,
                question_id=question_id,
                vote=-1
            )

            # calculating new score
            response = calculate_score(question_id, Question)
            if response:
                return response
        question = Question.objects.filter(id=question_id)
        if not question:
            return Response(
                went_wrong,
                status.HTTP_404_NOT_FOUND
            )
        question = question[0]
        question_serializer = QuestionSerializer(question)
        return Response(question_serializer.data)


class Unvote(APIView):
    '''Api view to unvote a question or answer'''

    # adding permissions for upvote api
    permission_classes = [IsAuthenticated]

    def get(self, request, question_id, answer_id=None):
        '''method for handle get requests'''

        if answer_id:
            # deleting vote object of loggedin user
            delete_vote_object(request.user, answer_id=answer_id)

            # calculating new score
            response = calculate_score(answer_id, Answer)
            if response:
                return response
        else:
            # deleting vote objects if there is any
            delete_vote_object(request.user, question_id=question_id)

            # calculating new score
            response = calculate_score(question_id, Question)
            if response:
                return response
        question = Question.objects.filter(id=question_id)
        if not question:
            return Response(
                went_wrong,
                status.HTTP_404_NOT_FOUND
            )
        question = question[0]
        question_serializer = QuestionSerializer(question)
        return Response(question_serializer.data)
