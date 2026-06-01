from django.db import transaction

@transaction.atomic
def create_domain_entity(*, name: str) -> object:
    """Example Service Layer mutation handler wrapping transaction execution."""
    # Write safe state modifications here
    pass
