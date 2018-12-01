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

        if 'image_name' not in data:
            return JsonResponse({'status': 'success', 'error': {'mssg': 'Missing Image Name'}})
        if 'pointer_x' not in data:
            return JsonResponse({'status': 'success', 'error': {'mssg': 'Missing Pointer X'}})
        if 'pointer_y' not in data:
            return JsonResponse({'status': 'success', 'error': {'mssg': 'Missing Pointer Y'}})
        if 'box_width' not in data:
            return JsonResponse({'status': 'success', 'error': {'mssg': 'Missing Bounding Box Width'}})
        if 'box_height' not in data:
            return JsonResponse({'status': 'success', 'error': {'mssg': 'Missing Bounding Box Height'}})
        if 'label' not in data:
            return JsonResponse({'status': 'success', 'error': {'mssg': 'Missing Image Label'}})

        image = data['image_name']
        pointer_x = data['pointer_x']
        pointer_y = data['pointer_y']
        box_width = data['box_width']
        box_height = data['box_height']
        label = data['label']

        image_data = Image.objects.filter(name=image)

        if not image_data:
            return JsonResponse({'status': 'success', 'error': {'mssg': 'Image not found'}})

        BoundingBox.objects.create(image=image_data[0],
                                   pointer_x=pointer_x,
                                   pointer_y=pointer_y,
                                   box_width=box_width,
                                   box_height=box_height,
                                   label=label)

        return JsonResponse({'status': 'success'})


