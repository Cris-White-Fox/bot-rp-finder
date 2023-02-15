from django.contrib import admin
from django.utils.safestring import mark_safe
from myapp import models



# Register your models here.
@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("profile", "image_id", "image_url", "image_tag")


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("uid", "name", "text", "images", "nsfw", "last_activity")

    @admin.display(description="Изображения")
    def images(self, instance: models.Profile):
        return mark_safe(' '.join(img.image_tag() for img in instance.image_set.all()))


@admin.register(models.Interaction)
class InteractionsAdmin(admin.ModelAdmin):
    list_display = ("initiator", "subject", "result", "datetime")