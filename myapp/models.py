from datetime import datetime
from django.db import models
from django.utils.safestring import mark_safe


# Create your models here.
class Profile(models.Model):
    uid = models.IntegerField(verbose_name="Идентификатор пользователя", unique=True)
    name = models.TextField(verbose_name="Имя", default="")
    text = models.TextField(verbose_name="Текст", default="")
    nsfw = models.BooleanField(verbose_name="Контент 18+", default=False)
    last_activity = models.DateTimeField(verbose_name="Дата последней активности", auto_now_add=True, null=True)

    def get_next_profile(self):
        interacted = Interaction.objects.filter(initiator=self.id).values_list("subject", flat=True)
        return Profile.objects.exclude(pk__in=interacted).exclude(pk=self.pk).order_by('-last_activity').first()

    def profile_changed(self):
        Interaction.objects.filter(subject=self).delete()

    def update_activity(self):
        self.last_activity = datetime.now()
        self.save()

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self) -> str:
        return f"Пользователь: {self.name} - {self.uid} ({self.last_activity})"


class Image(models.Model):
    profile = models.ForeignKey(Profile, verbose_name="Профиль владельца", on_delete=models.CASCADE)
    image_id = models.TextField(verbose_name="Идентификатор изображения", default="")
    image_url = models.TextField(verbose_name="ссылка на оригинал изображения", default="")

    def image_tag(self):
        if self.image_url:
            return mark_safe('<img src="%s" style="width: 90px; height:90px;" />' % self.image_url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = "Изображение анкеты"
        verbose_name_plural = "Изображения анкет"

    def __str__(self) -> str:
        return f"Изображение: {self.image_id} ({self.image_url})"


class Interaction(models.Model):
    initiator = models.ForeignKey(Profile, verbose_name="Инициатор", related_name='interaction_initiator', on_delete=models.CASCADE)
    subject = models.ForeignKey(Profile, verbose_name="Субъект", related_name='interaction_subject', on_delete=models.CASCADE)
    result = models.BooleanField(verbose_name="Результат взаимодействия")
    viewed = models.BooleanField(verbose_name="Просмотрено", default=False)
    datetime = models.DateTimeField(verbose_name="Дата взаимодействия", auto_now_add=True, blank=True)

    class Meta:
        verbose_name = "Взаимодействие пользователей"
        verbose_name_plural = "Взаимодействия пользователей"
        unique_together = ['initiator', 'subject']

    def __str__(self) -> str:
        return f"Взаимодействие: {self.initiator} - {self.subject} ({self.result})"