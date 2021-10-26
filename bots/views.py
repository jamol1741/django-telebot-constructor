from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .bot import process_updates
from .models import Bot


@csrf_exempt
def process_telegram_updates(request, bot_token):
    print(request.get_full_path())
    if request.method == "POST":
        try:
            bot = Bot.objects.get(token=bot_token)
            data = request.body.decode('utf-8')
            process_updates.bot = bot.token
            process_updates.run(data)
            return JsonResponse({}, status=200)
        except Bot.DoesNotExist:
            return JsonResponse({'detail': 'Invalid token'}, status=400)
    elif request.method == "GET":
        return JsonResponse({'detail': 'Method not allowed'}, status=405)
