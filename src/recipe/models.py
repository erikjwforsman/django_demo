from django.db import models

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as g_l
# Create your models here.


def upload_location(instance, filename, **kwargs):
    file_path = "recipe/{author_id}/{title}-{filename}".format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path
    #Joku ongelma pathissa

class Ohje(models.Model):
    class Dishes(models.TextChoices):
        ALKUPALA = "ALKUPALA", g_l("Alkupala")
        PÄÄRUOKA = "PÄÄRUOKA", g_l("Pääruoka")
        JÄLKIRUOKA = "JÄLKIRUOKA", g_l("Jälkiruoka")
        JUOMA = "JUOMA", g_l("Juoma")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    dish = models.CharField(max_length=12, choices=Dishes.choices, default=Dishes.PÄÄRUOKA)
    cooking_time = models.PositiveIntegerField(null=False, blank=False)
    body = models.TextField(max_length=100000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=False, blank=False) #Mitchillä true molemmissa
    ingredients = models.CharField(max_length=500, null=False, blank=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

@receiver(post_delete, sender=Ohje)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_ohje_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.author.username +"-"+ instance.title)

pre_save.connect(pre_save_ohje_receiver, sender=Ohje)


class Comment(models.Model):
    recipe_commented = models.ForeignKey("recipe.Ohje", on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    author = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="date published")

    def save(self, *agrs, **kwargs):
        super().save()

    def __str__(self):
        return self.text
