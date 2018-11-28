from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import BoundingBox, Image
def index(request):
    return HttpResponse("Hi")

@csrf_exempt
def submitData(request):
    if request.method == 'GET':
        return HttpResponse("Hello, world. You're at the polls index.")
    elif request.method == 'POST':
        data = request.POST.dict()

        image = data['image_name']
        pointer_x = data['pointer_x']
        pointer_y = data['pointer_y']
        box_width = data['box_width']
        box_height = data['box_height']
        label = data['label']

        bounding_box = BoundingBox()

        return JsonResponse({'status':'success'})
