from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import MoviesSerializer
from .models import Movie
import sys
from rest_framework.decorators import action

class MoviesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()              # ✅ required
    serializer_class = MoviesSerializer         # ✅ required

    @action(detail=False, methods=["get"], url_path='suggest')
    def suggetions_titles(self, request):
        query = request.query_params.get('q', "")
        if query:
            movies = Movie.objects.filter(title__istartswith=query)[:10]
            serializer = MoviesSerializer(movies, many=True)
            return Response(serializer.data)
        return Response([])

        
    # def list(self, request):
    #     queryset = self.get_queryset()          # ✅ better than hardcoding
    #     serializer = self.get_serializer(queryset, many=True)
    #     # print(serializer.data, file=sys.stderr)
    #     return Response(serializer.data)
