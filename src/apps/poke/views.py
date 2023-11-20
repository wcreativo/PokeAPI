from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BerriesResponseSerializer
from .utils import generate_statistics, get_all_berries_info


class BerryView(APIView):
    def get(self, request):
        names, growth_times = get_all_berries_info()
        berries_stats = generate_statistics(growth_times)
        berries_stats["berries_names"] = names
        serializer = BerriesResponseSerializer(data=berries_stats)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.error_messages)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
