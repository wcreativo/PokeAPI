import os

import matplotlib.pyplot as plt
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BerriesResponseSerializer
from .utils import generate_statistics, get_all_berries_info


class BerryView(APIView):
    """
    API endpoint to retrieve statistics and details about berry growth times.

    This view class fetches information about berry growth times and calculates statistics.
    It utilizes 'get_all_berries_info' to gather names and growth times,
    and 'generate_statistics' to compute statistical measures.
    The resulting statistics are then serialized using 'BerriesResponseSerializer'.

    Methods:
    - get(self, request): Retrieves berry information, calculates statistics, and serializes the data.

    Endpoint Behavior:
    - GET request: Fetches information about berry growth times and statistics.
        - Returns a serialized response containing berry names, growth times, and statistics.
        - Status codes:
            - 200 OK: Successful response with serialized data.
            - 500 INTERNAL SERVER ERROR: If there are issues with serialization.
    """

    def get(self, request):
        names, growth_times = get_all_berries_info()
        if growth_times:
            berries_stats = generate_statistics(growth_times)
            berries_stats["berries_names"] = names
            serializer = BerriesResponseSerializer(data=berries_stats)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "There is not berries"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HistogramImageView(APIView):
    def get(self, request):
        names, growth_times = get_all_berries_info()
        fig, ax = plt.subplots()
        bins = range(0, max(growth_times) + 1, 1)
        ax.hist(growth_times, bins=bins, edgecolor="black")
        ax.set_xlabel("Growth Cycles")
        ax.set_ylabel("Frequency")
        ax.set_title("Frequency Histogram of Berry Growth Times in Pokémon")
        ax.grid(True)

        image_path = os.path.join(settings.MEDIA_ROOT, "histogram.png")

        plt.savefig(image_path)

        # Render the HTML template with the image
        context = {"image_path": image_path}
        template = loader.get_template("poke/histogram_display.html")
        html = template.render(context)

        return HttpResponse(html)
