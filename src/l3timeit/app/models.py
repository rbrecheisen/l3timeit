import os
import uuid
from django.db import models
from django.dispatch import receiver


class ImageModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    file_obj = models.FileField(upload_to='')
    file_name = models.CharField(max_length=1024, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    downloaded_at = models.DateTimeField(null=True)
    done_at = models.DateTimeField(null=True)
    finished = models.BooleanField(default=False)
    seconds = models.IntegerField(null=True)


@receiver(models.signals.pre_save, sender=ImageModel)
def image_pre_save(sender, instance, **kwargs):
    """
    Before we save the file model, we generate a UUID and set the 'id' and
    'file_obj.name' with it so that the file that gets saved to disk is named
    according to the UUID.
    """
    if not instance.id:
        file_id = str(uuid.uuid4())
        instance.id = file_id


@receiver(models.signals.post_delete, sender=ImageModel)
def image_post_delete(sender, instance, **kwargs):
    """
    In early versions of Django, the local file referred to by the FileField would be
    deleted automatically whenever the model object was deleted. In recent versions,
    this no longer happens so you need to do this yourself.
    """
    if instance.file_obj:
        if os.path.isfile(instance.file_obj.path):
            os.remove(instance.file_obj.path)
