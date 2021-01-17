from rest_framework import serializers
from django.contrib.auth.models import User
from stackoverflow.models import Question, Answer, Comment, Vote, Tag
from stackoverflow.helper import attach_profile, calculate_expiry


class UserInfoSerializer(serializers.Serializer):
    '''User Info serializer will be used by
    Token Serializer or listing users'''

    username = serializers.CharField()
    role = serializers.CharField()
    id = serializers.IntegerField()
    created = serializers.DateTimeField()
    profilePhoto = serializers.CharField()

    def to_representation(self, value):
        '''method to customize read operation'''

        if not type(value) == dict:
            # attaching profile fields with user
            query = attach_profile(User.objects.filter(username=value))
            if not query:
                raise serializers.ValidationError(
                    {'message': 'somthing webt wrong'}
                )
            return query[0]
        return value


class TokenSerializer(serializers.Serializer):
    '''Token Serializer will contain token and user info'''

    message = serializers.CharField()
    expiresAt = serializers.IntegerField()
    token = serializers.CharField()

    # user info serializer nested inside token
    userInfo = UserInfoSerializer()


class SignupSerializer(serializers.Serializer):
    '''Signup serializer will be used by signup API'''

    username = serializers.CharField()
    password = serializers.CharField()
    passwordConfirmation = serializers.CharField()

    def validate(self, data):
        '''method for validating data'''

        if data['password'] != data['passwordConfirmation']:
            raise serializers.\
                ValidationError({'message': 'password did not match'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.\
                ValidationError({'message': 'username already exists'})
        return data

    def create(self, validated_data):
        '''method for crete objects in database invoked when save called'''

        user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password']
            )

        # required format of data via frontend
        data = {
            'message': "User created!",
            'expiresAt': calculate_expiry(),
            'token': user.auth_token.key,
            'userInfo': {
                'username': user.username,
                'role': user.profile.role,
                'id': user.id,
                'created': user.date_joined,
                'profilePhoto': user.profile.photo
                }
            }
        token_serializer = TokenSerializer(data=data)
        return token_serializer


class AuthenticateSerializer(serializers.Serializer):
    '''Authenticate Serializer will be used by authenticate api'''

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        '''method for validating data'''

        user = User.objects.filter(
            username=data['username'],
        )
        if not user:
            raise serializers.ValidationError(
                {'message': 'user does not exists'}
            )
        user = user[0]
        if not user.check_password(data['password']):
            raise serializers.ValidationError(
                {'message': 'wrong password'}
            )

        # required format of data via frontend
        data = {
            'message': "Authentication successful!",
            'expiresAt': calculate_expiry(),
            'token': user.auth_token.key,
            'userInfo': {
                'username': user.username,
                'role': user.profile.role,
                'id': user.id,
                'created': user.date_joined,
                'profilePhoto': user.profile.photo
                }
            }
        token_serializer = TokenSerializer(data=data)
        return token_serializer


class TagList(serializers.RelatedField):
    '''
    To only get only the names
    of tag
    '''

    def to_representation(self, value):
        '''
        returns the name in
        form of list
        '''
        return value.name


class VoteSerializer(serializers.ModelSerializer):
    '''
    Model Serializer for vote field
    '''

    class Meta:
        model = Vote
        fields = ['user', 'vote']


class CommentSerializer(serializers.ModelSerializer):
    '''
    gives the json object regarding
    comment field
    '''

    author = UserInfoSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    '''
    For getting the answers
    '''
    votes = VoteSerializer(many=True)
    comments = CommentSerializer(many=True)
    author = UserInfoSerializer()

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    '''
    Below are the things related to
    Question
    '''

    tags = TagList(many=True, read_only='True')
    votes = VoteSerializer(many=True)
    comments = CommentSerializer(many=True)
    answers = AnswerSerializer(many=True)
    author = UserInfoSerializer()

    class Meta:
        model = Question
        fields = '__all__'


class TagSerializer(serializers.Serializer):
    '''
    returns all the tags used in question
    '''

    _id = serializers.CharField(source='tags__name')
    count = serializers.IntegerField()
    field = '__all__'


class QuestionPostSerializer(serializers.ModelSerializer):
    '''
    Post the question in same format
    add the tags with question id
    by overriding create method
    '''

    tags = serializers.ListField(child=serializers.CharField(max_length=15))

    class Meta:
        model = Question
        fields = ['title', 'author', 'text', 'tags']

    def create(self, validated_data):
        tag_data = validated_data.pop('tags')
        question = Question.objects.create(**validated_data)
        for tag in tag_data:
            t = Tag.objects.create(name=tag)
            t.save()
            t.question.add(question.id)
        return question
