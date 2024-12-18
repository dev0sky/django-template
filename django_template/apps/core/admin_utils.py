from django.contrib.contenttypes.models import ContentType
from core.models import Log

def log_admin_action(request, obj, form, change):
    obj.save()

    log_type = 'update' if change else 'create'

    content_type = ContentType.objects.get_for_model(obj)

    if form.has_changed():
        changed_fields = form.changed_data
        changed_fields_str = ', '.join(changed_fields)

        log_name = f'{obj.__class__.__name__} {obj} was {log_type}d'
        log_message = f'From admin panel. \nChanged fields: {changed_fields_str}'
    else:
        log_name = f'{obj.__class__.__name__} {obj} was {log_type}d'
        log_message = f'{obj.__class__.__name__} {obj} was {log_type}d from admin panel.'

    Log.objects.create(
        content_type=content_type,
        object_id=obj.id,
        name=log_name,
        description=log_message,
        log_type=log_type,
        user=request.user,
        ip_address=request.META.get('REMOTE_ADDR'),
        model=obj.__class__.__name__,
        content_object=obj,
    )
