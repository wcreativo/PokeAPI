from rest_framework import serializers


class BerriesResponseSerializer(serializers.Serializer):
    berries_names = serializers.ListField(child=serializers.CharField())
    min_growth_time = serializers.FloatField()
    median_growth_time = serializers.FloatField()
    max_growth_time = serializers.FloatField()
    variance_growth_time = serializers.FloatField()
    mean_growth_time = serializers.FloatField()
    frequency_growth_time = serializers.DictField()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        readable_frequency = []
        for x, y in representation["frequency_growth_time"].items():
            readable_frequency.append({"growth_time_cycles": x, "berry_count": y})
        representation["frequency_growth_time"] = readable_frequency
        representation["min_growth_time"] = f"{representation['min_growth_time']:.1f} cycles"
        representation["median_growth_time"] = f"{representation['median_growth_time']:.1f} cycles"
        representation["max_growth_time"] = f"{representation['max_growth_time']:.1f} cycles"
        representation["variance_growth_time"] = f"{representation['variance_growth_time']:.1f} cycles"
        representation["mean_growth_time"] = f"{representation['mean_growth_time']:.1f} cycles"
        return representation
