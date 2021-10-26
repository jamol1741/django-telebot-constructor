from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telebot import types

from .bot import bot
from .models import Bot


@csrf_exempt
def process_telegram_updates(request, bot_token):
    if request.method == "POST":
        try:
            print(bot.message_handlers)
            bot.token = Bot.objects.get(token=bot_token).token
            update = types.Update.de_json(request.body.decode('utf-8'))
            print(update)
            bot.process_new_updates([update])
            return JsonResponse({}, status=200)
        except Bot.DoesNotExist:
            return JsonResponse({'detail': 'Invalid token'}, status=400)
    elif request.method == "GET":
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
