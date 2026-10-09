from django.contrib.postgres.search import SearchVector, SearchQuery
from apps.businesses.models import Business


class SearchService:
    @staticmethod
    def search_businesses(query_text: str):
        """
        فاز ۱: Full-Text Search با PostgreSQL. 
        در فازهای بعد بدون تغییر در Views، این متد می‌تواند به ElasticSearch متصل شود.
        """
        if not query_text:
            return Business.objects.none()

        vector = SearchVector('title', weight='A') + SearchVector('description', weight='B')
        query = SearchQuery(query_text)

        return Business.objects.annotate(search=vector).filter(search=query)