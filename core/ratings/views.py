from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Rating, Vote
from .serializers import RatingSerializer, VoteSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        rating = Rating.objects.get(pk=serializer.validated_data['rating'].id)
        user = request.user
        try:
            vote = Vote.objects.get(rating=rating, user=user)
            vote.value = serializer.validated_data['value']
            vote.save()
            return Response({'message': 'Vote updated successfully'}, status=status.HTTP_200_OK)
        except Vote.DoesNotExist:
            serializer.save(user=user)
            return Response({'message': 'Vote created successfully'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        rating = Rating.objects.get(pk=self.get_object().rating.id)
        try:
            vote = Vote.objects.get(rating=rating, user=user)
            vote.delete()
            return Response({'message': 'Vote deleted successfully'}, status=status.HTTP_200_OK)
        except Vote.DoesNotExist:
            return Response({'message': 'Vote not found'}, status=status.HTTP_404_NOT_FOUND)
