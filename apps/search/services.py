import difflib
from django.db.models import Q
from apps.businesses.models import Business, BusinessStatus
from apps.categories.models import Category
from apps.catalog.models import CentralCatalogItem


class IntelligentSearchService:
    @staticmethod
    def calculate_similarity(s1: str, s2: str) -> float:
        """
        محاسبه میزان شباهت املایی بین دو متن (پشتیبانی کامل از غلط‌های املایی مانند فرهگ -> فرهنگ)
        """
        if not s1 or not s2:
            return 0.0
        return difflib.SequenceMatcher(None, s1.lower(), s2.lower()).ratio()

    @classmethod
    def live_search(cls, query_text: str, limit_per_section=5):
        query = query_text.strip()
        if not query or len(query) < 2:
            return {'businesses': [], 'categories': [], 'catalog_items': []}

        # ۱. تفکیک کلمات تایپ‌شده توسط کاربر
        words = [w for w in query.split() if len(w) >= 2]
        if not words:
            return {'businesses': [], 'categories': [], 'catalog_items': []}

        # -------------------------------------------------------------
        # بخش اول: جستجوی دسته‌بندی‌ها (Categories) با Fuzzy Matching
        # -------------------------------------------------------------
        all_categories = Category.objects.filter(is_active=True)
        matched_categories = []

        for cat in all_categories:
            cat_words = cat.name.split()

            # محاسبه شباهت کلمه به کلمه (مثلاً مقایسه «فرهگ» با تک‌تک کلمات دسته‌بندی)
            word_scores = []
            for w in words:
                best_word_score = max([cls.calculate_similarity(w, cw) for cw in cat_words] or [0])
                # اگر کلمه به صورت ناقص هم در کلمه هدف وجود داشت (Sub-match)
                if any(w in cw or cw in w for cw in cat_words):
                    best_word_score = max(best_word_score, 0.85)
                word_scores.append(best_word_score)

            avg_score = sum(word_scores) / len(word_scores) if word_scores else 0
            full_score = cls.calculate_similarity(query, cat.name)
            final_score = max(full_score, avg_score)

            # آستانه قبول شباهت املایی (۶۰ درصد به بالا)
            if final_score >= 0.60:
                matched_categories.append({
                    'id': cat.id,
                    'name': cat.name,
                    'slug': cat.slug,
                    'url': f"/categories/{cat.slug}/",
                    'icon': cat.icon or '🏢',
                    'similarity': int(final_score * 100)
                })

        # مرتب‌سازی بر اساس بالاترین میزان شباهت
        matched_categories = sorted(matched_categories, key=lambda x: x['similarity'], reverse=True)[:limit_per_section]

        # -------------------------------------------------------------
        # بخش دوم: جستجوی کسب‌وکارها (Businesses)
        # -------------------------------------------------------------
        # ساخت فیلتر اولیه دیتابیس (بر اساس ریشه کلمات برای سرعت بالا)
        q_filter = Q()
        for w in words:
            prefix = w[:len(w) - 1] if len(w) > 3 else w
            q_filter |= Q(title__icontains=prefix) | Q(description__icontains=prefix) | Q(
                category__name__icontains=prefix)

        businesses_qs = Business.objects.filter(
            status=BusinessStatus.APPROVED,
            is_active=True
        ).filter(q_filter).select_related('category')[:limit_per_section * 3]

        matched_businesses = []
        for b in businesses_qs:
            b_words = (b.title + " " + (b.category.name if b.category else "")).split()
            word_scores = [max([cls.calculate_similarity(w, bw) for bw in b_words] or [0]) for w in words]
            avg_score = sum(word_scores) / len(word_scores) if word_scores else 0

            title_score = cls.calculate_similarity(query, b.title)
            final_score = max(title_score, avg_score)

            if final_score >= 0.55:
                matched_businesses.append({
                    'id': b.id,
                    'title': b.title,
                    'category_name': b.category.name if b.category else '',
                    'slug': b.slug,
                    'url': f"/businesses/{b.slug}/",
                    'image_url': b.logo.url if b.logo else '/static/images/default-logo.png',
                    'similarity': int(final_score * 100)
                })

        matched_businesses = sorted(matched_businesses, key=lambda x: x['similarity'], reverse=True)[:limit_per_section]

        # -------------------------------------------------------------
        # بخش سوم: کالاها و خدمات مرکزی (Catalog Items)
        # -------------------------------------------------------------
        q_cat_filter = Q()
        for w in words:
            prefix = w[:len(w) - 1] if len(w) > 3 else w
            q_cat_filter |= Q(title__icontains=prefix)

        catalog_qs = CentralCatalogItem.objects.filter(q_cat_filter).select_related('category')[:limit_per_section * 2]
        matched_catalog = []

        for item in catalog_qs:
            item_words = item.title.split()
            word_scores = [max([cls.calculate_similarity(w, iw) for iw in item_words] or [0]) for w in words]
            avg_score = sum(word_scores) / len(word_scores) if word_scores else 0
            title_score = cls.calculate_similarity(query, item.title)
            final_score = max(title_score, avg_score)

            if final_score >= 0.55:
                matched_catalog.append({
                    'id': item.id,
                    'title': item.title,
                    'type_display': item.get_item_type_display(),
                    'category_name': item.category.name if item.category else '',
                    'url': f"/search/?q={item.title}",
                    'similarity': int(final_score * 100)
                })

        matched_catalog = sorted(matched_catalog, key=lambda x: x['similarity'], reverse=True)[:limit_per_section]

        return {
            'businesses': matched_businesses,
            'categories': matched_categories,
            'catalog_items': matched_catalog,
        }