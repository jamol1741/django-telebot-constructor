import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from telebot import TeleBot


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class Bot(BaseModel):
    token = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120)

    def __str__(self):
        return self.username

    def clean(self):
        api_url = settings.TELEGRAM_BASE_URL.format(token=self.token) + 'setwebhook'
        print(api_url)
        params = {
            'url': f"{settings.HOST}/bot/{self.token}/"
        }
        r = requests.get(api_url, params=params)
        if r.status_code == 200:
            pass
        else:
            raise ValidationError(f"Could not set webhook. Please check params. {r.content}")


class User(BaseModel):
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE)
    tgid = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, null=True, blank=True)
    username = models.CharField(max_length=120, null=True, blank=True)


# @receiver(pre_save, sender=Bot)
# def pre_save_bot(sender, instance: Bot, *args, **kwargs):
#     bot = TeleBot(instance.token)
#     me = bot.get_me()
#     instance.name = me.first_name
#     instance.username = me.username
#     del bot

@receiver(post_delete, sender=Bot)
def delete_webhook(sender, instance: Bot, *args, **kwargs):
    bot = TeleBot(instance.token)
    bot.delete_webhook(drop_pending_updates=True)
    del bot
