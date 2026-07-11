from django.db import models

# Place all extraction queries / business reads inside Selectors.

def get_active_records(*, limit: int = 100) -> list:
    """Example selector isolating database query reads."""
    # Example usage:
    # return MyModel.objects.filter(is_active=True)[:limit]
    return []
