from core.models import ContactMessage


def admin_panel_context(request):
    """Inject unread message count into every template for staff users."""
    if request.user.is_authenticated and request.user.is_staff:
        return {
            'unread_count': ContactMessage.objects.filter(is_read=False).count()
        }
    return {'unread_count': 0}
