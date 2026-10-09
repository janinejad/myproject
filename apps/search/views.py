from django.http import JsonResponse
from apps.search.services import IntelligentSearchService

def live_search_api(request):
    query = request.GET.get('q', '')
    results = IntelligentSearchService.live_search(query)
    return JsonResponse(results)