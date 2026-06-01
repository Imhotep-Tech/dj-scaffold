from django.db import models

# Place all extraction queries / business reads inside Selectors.

def get_active_records(*, limit: int = 100) -> models.QuerySet:
    """Example selector isolating database query reads."""
    return models.QuerySet().none()
