from django.contrib import admin
from django.utils.html import format_html
from .models import ContactSubmission, Portfolio, SocialMedia, SiteSetting


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'country', 'service', 'budget', 'timeline', 'submitted_at', 'is_read']
    list_filter = ['service', 'country', 'budget', 'timeline', 'is_read', 'submitted_at']
    search_fields = ['name', 'email', 'phone', 'country', 'message']
    readonly_fields = ['submitted_at']
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Mark selected as read'

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = 'Mark selected as unread'


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_date', 'is_active', 'image_preview']
    list_filter = ['category', 'is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['created_date', 'image_preview']
    fieldsets = [
        ('Project Info', {'fields': ['title', 'description', 'category']}),
        ('Media & URL', {'fields': ['image', 'image_preview', 'project_url']}),
        ('Status', {'fields': ['is_active', 'created_date']}),
    ]

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:100px;border-radius:8px;" />', obj.image.url)
        return '-'
    image_preview.short_description = 'Preview'


@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'icon_class', 'is_active', 'order']
    list_editable = ['order', 'is_active']


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'value']
    search_fields = ['key']
