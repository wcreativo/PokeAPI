from rest_framework import serializers


class BerriesResponseSerializer(serializers.Serializer):
    berries_names = serializers.ListField(child=serializers.CharField())
    min_growth_time = serializers.FloatField()
    median_growth_time = serializers.FloatField()
    max_growth_time = serializers.FloatField()
    variance_growth_time = serializers.FloatField()
    mean_growth_time = serializers.FloatField()
    frequency_growth_time = serializers.DictField()
