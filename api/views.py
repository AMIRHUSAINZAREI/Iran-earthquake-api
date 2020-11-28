from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import EarthQuake
from .serializers import EarthQuakeSerializer
from .functions import update_earthquake_model, init_data


def all_earthquakes(request):
    query_set = EarthQuake.objects.all()
    if len(query_set) == 0:
        init_data()
        query_set = EarthQuake.objects.all()

    serializer = EarthQuakeSerializer(query_set, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)


def last_n_earthquake(request, n):
    query_set = EarthQuake.objects.all()
    if len(query_set) == 0:
        init_data()
    if n > len(EarthQuake.objects.all()):
        serializer = EarthQuakeSerializer(query_set, many=True)
        data = serializer.data
        return JsonResponse(data, safe=False)

    query_set = EarthQuake.objects.all()[len(EarthQuake.objects.all())-n:]
    serializer = EarthQuakeSerializer(query_set, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)

def magnitude_gte(request, m):
    query_set = EarthQuake.objects.all()
    if len(query_set) == 0:
        init_data()
        query_set = EarthQuake.objects.all()
    m = float(m)
    m_query_set = EarthQuake.objects.filter(magnitude__gte=m)
    serializer = EarthQuakeSerializer(m_query_set, many=True)
    data = serializer.data
    return JsonResponse(data, safe=False)
