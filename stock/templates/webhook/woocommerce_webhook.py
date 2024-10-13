from django.http import JsonResponse
import json

def woocommerce_webhook(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            # Procesa el payload aquí
            print(payload)
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'method not allowed'}, status=405)
