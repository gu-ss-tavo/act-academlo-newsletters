from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from newsletter.models import Newsletter

from .models import CustomUser
from .serializers import CustomUserSerializer, NewsletterUsersSerializer

# Create your views here.
class RegisterUserViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = CustomUserSerializer
    model = CustomUser

class CustomUserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated,]
    serializer_class = CustomUserSerializer
    model = CustomUser

    def get_queryset(self):
        self.queryset = CustomUser.objects.filter(id=self.request.user.id)
        return super().get_queryset()

    @action(detail=False, methods=['GET', 'POST'], serializer_class=NewsletterUsersSerializer)
    def newsletter_subscriptions(self, request):
        if request.method == 'GET':
            user = request.user
            newsletters = Newsletter.objects.filter(users__id=user.id)
            newsletter_serialized = NewsletterUsersSerializer(newsletters, many=True)

            if not newsletters or not newsletters.count() > 0:
                return Response(status=status.HTTP_200_OK,
                                data={
                                    'message':'No suscriptions'
                                })
            return Response(status=status.HTTP_200_OK, data=newsletter_serialized.data)

        elif request.method == 'POST':
            id_to_delete = request.data.get('delete_by_id')

            if id_to_delete:
                newsletter_found = Newsletter.objects.filter(id=id_to_delete).first()

                if newsletter_found:
                    users = (newsletter_found.users).all()
                    users = list(users)
                    users.remove(request.user)

                    newsletter_found.users.set(users)
                    newsletter_found.save()

                    return Response(status=status.HTTP_200_OK,
                                    data={
                                        'message':f'Deleted subscription: {newsletter_found.name}'
                                    })
            return Response(status=status.HTTP_404_NOT_FOUND,
                        data={
                            'message':'No such subscription exists'
                        })

    @action(detail=False, methods=['GET', 'POST'], serializer_class=NewsletterUsersSerializer)
    def newsletter_votes(self, request):
        if request.method == 'GET':
            user = request.user
            newsletters = Newsletter.objects.filter(votes__id=user.id)
            newsletter_serialized = NewsletterUsersSerializer(newsletters, many=True)

            if not newsletters or not newsletters.count() > 0:
                return Response(status=status.HTTP_200_OK,
                                data={
                                    'message':'No votes'
                                })
            return Response(status=status.HTTP_200_OK, data=newsletter_serialized.data)

        elif request.method == 'POST':
            id_to_delete = request.data.get('delete_by_id')

            if id_to_delete:
                newsletter_found = Newsletter.objects.filter(id=id_to_delete).first()

                if newsletter_found:
                    votes = (newsletter_found.votes).all()
                    votes = list(votes)
                    votes.remove(request.user)

                    newsletter_found.votes.set(votes)
                    newsletter_found.save()

                    return Response(status=status.HTTP_200_OK,
                                    data={
                                        'message':f'Deleted vote: {newsletter_found.name}'
                                    })
            return Response(status=status.HTTP_404_NOT_FOUND,
                        data={
                            'message':'There is no such vote'
                        })


