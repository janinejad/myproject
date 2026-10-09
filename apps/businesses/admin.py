from django.contrib import admin
from apps.businesses.models import Business, BusinessWorkingHour, BusinessSocial, BusinessStatus


class BusinessWorkingHourInline(admin.TabularInline):
    model = BusinessWorkingHour
    min_num = 0
    max_num = 7


class BusinessSocialInline(admin.TabularInline):
    model = BusinessSocial


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'status', 'is_active', 'views_count', 'created_at')
    list_filter = ('status', 'is_active', 'category', 'created_at')
    search_fields = ('title', 'description', 'phone', 'mobile', 'address', 'owner__username', 'owner__phone_number')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    inlines = [BusinessWorkingHourInline, BusinessSocialInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('owner', 'title', 'slug', 'category', 'sub_categories', 'description')
        }),
        ('تصاویر', {
            'fields': ('logo', 'cover_image')
        }),
        ('اطلاعات تماس و موقعیت', {
            'fields': ('address', 'phone', 'mobile', 'website', 'latitude', 'longitude')
        }),
        ('وضعیت انتشار و آمار', {
            'fields': ('status', 'is_active', 'views_count', 'created_at', 'updated_at')
        }),
    )

    actions = ['approve_businesses', 'reject_businesses', 'suspend_businesses']

    @admin.action(description='تأیید کسب‌وکارهای انتخاب‌شده')
    def approve_businesses(self, request, queryset):
        updated = queryset.update(status=BusinessStatus.APPROVED)
        self.message_user(request, f"{updated} کسب‌وکار با موفقیت تأیید شدند.")

    @admin.action(description='رد کسب‌وکارهای انتخاب‌شده')
    def reject_businesses(self, request, queryset):
        updated = queryset.update(status=BusinessStatus.REJECTED)
        self.message_user(request, f"{updated} کسب‌وکار رد شدند.")

    @admin.action(description='معلق کردن کسب‌وکارهای انتخاب‌شده')
    def suspend_businesses(self, request, queryset):
        updated = queryset.update(status=BusinessStatus.SUSPENDED)
        self.message_user(request, f"{updated} کسب‌وکار معلق شدند.")