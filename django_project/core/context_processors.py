from .models import SocialMedia


def social_links(request):
    return {
        'social_links': SocialMedia.objects.filter(is_active=True),
    }
