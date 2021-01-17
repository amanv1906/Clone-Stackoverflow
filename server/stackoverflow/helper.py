from django.db.models import F
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
from stackoverflow.models import Vote
import datetime

# something went wrong message
went_wrong = {'message': 'something went wrong'}


def attach_profile(query):
    '''function to convert users to required format via frontend'''

    # annotate query set with required field and sort
    # them on the basis of creation time
    query_set = query.values('username', 'id').\
        annotate(
            role=F('profile__role'),
            created=F('date_joined'),
            profilePhoto=F('profile__photo')
        ).\
        order_by('-date_joined')
    return query_set


def calculate_score(id, model):
    '''function to calculate answers/question score
    after added remove of undo vote operations'''

    # checking if instance exists of not
    instance = model.objects.filter(id=id)

    if not instance:
        return Response(
            {'message': 'Voted object does not exists'},
            status.HTTP_404_NOT_FOUND
        )
    instance = instance[0]

    # aggrerating votes and assigning to instance score
    instance.score = instance.votes.aggregate(Sum('vote'))['vote__sum'] or 0
    instance.save()


def delete_vote_object(user, answer_id=None, question_id=None):
    '''function to delete vote object after up/down/un operations'''

    if answer_id:
        # deleting vote object for given answer id
        Vote.objects.filter(
            user=user,
            answer_id=answer_id
        ).delete()
    else:
        # deleting vote object for given question id
        Vote.objects.filter(
            user=user,
            question_id=question_id
        ).delete()


def calculate_expiry():
    '''function to return expiry date of day 7 from today'''

    expiry_date = datetime.datetime.now() + datetime.timedelta(days=7)
    expires_at = datetime.datetime.timestamp(expiry_date)
    return int(expires_at)
