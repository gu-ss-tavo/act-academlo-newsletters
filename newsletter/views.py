from rest_framework import serializers, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import NewsletterSerializer, UserNewsletterSerializer, VoteNewsletterSerializer
from .models import Newsletter

from user.serializers import CustomUserSerializer
from tag.serializers import TagSerializer

# Create your views here.
class NewsletterViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    '''
    * @action 'tags'
    --- espacio donde se muestran las tags asociadas al 'newsletter'
    '''
    @action(detail=True, methods=['GET'])
    def tags(self, request, pk=None):
        tags = self.get_object().tags
        serialized = TagSerializer(tags, many=True)

        if not tags or not tags.count() > 0:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={
                                'message':'This newsletter has no tags'
                            })
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    '''
    * @action 'subscribed_users'
    --- espacio donde se muestran los usuarios suscritos
    --- espacio para actualizar el estado de nuestra suscripción
    --- entrada: BooleanField
    '''
    @action(detail=True, methods=['GET', 'POST'], serializer_class=UserNewsletterSerializer)
    def subscribed_users(self, request, pk=None):
        obj = self.get_object()
        vote_count = (obj.votes).all().count()
        if request.method == 'POST':
            new_status = request.data.get('status').__str__().lower() == 'true'
            is_different = new_status != (request.user in list((obj.users).all()))

            if vote_count >= obj.meta and is_different:
                users = (obj.users).all()
                users = list(users)

                if new_status:
                    users.append(request.user)
                else:
                    users.remove(request.user)

                obj.users.set(users)
                obj.save()

        users = self.get_object().users
        serialized = CustomUserSerializer(users, many=True)

        if not users or not users.count() > 0:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={
                                'message':'This newsletter has no subscribed users'
                            })
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    '''
    * @action 'vote'
    --- espacio para confirmar o eliminar voto
    --- entrada: CharField
    --- --- @param: 'ok'
    --- --- @param: 'remove'
    '''
    @action(detail=True, methods=['GET', 'POST'], serializer_class=VoteNewsletterSerializer)
    def vote(self, request, pk=None):
        obj = self.get_object()

        if request.method == 'POST':
            if request.data.get('vote'):
                user_vote = (obj.votes).all()
                user_vote = list(user_vote)
                option = None

                if 'ok' == request.data.get('vote').lower():
                    if not request.user in user_vote:
                        option = 'ok'
                        user_vote.append(request.user)
                elif 'remove' == request.data.get('vote').lower():
                    if request.user in user_vote:
                        option = 'remove'
                        user_vote.remove(request.user)
                else:
                    for vote in user_vote:
                        if vote.email == request.user.email:
                            raise serializers.ValidationError(detail='\'remove\' needed to delete your vote', code='negation')

                    raise serializers.ValidationError(detail='\'ok\' needed to confirm your vote', code='negation')

                obj.votes.set(user_vote)
                obj.save()

                message = None
                if option == 'ok':
                    message = 'Thanks for voting'
                elif option == 'remove':
                    message = 'Elliminate vote'

                if message:
                    return Response(status=status.HTTP_202_ACCEPTED,
                                    data={
                                        'message': message
                                    })

        votes_serialized = CustomUserSerializer(obj.votes, many=True)
        for vote in votes_serialized.data:
            if vote.get('email') == request.user.email:
                return Response(status=status.HTTP_200_OK,
                                data={
                                    'message': 'Voted / send \'remove\' to remove your vote'
                                })

        return Response(status=status.HTTP_200_OK,
                        data={
                            'message': 'Not voted / send \'ok\' to confirm'
                        })
