# capa de vista/presentación

from django.http import HttpRequest, QueryDict
from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# tambien hacemos una comunicacion aparte con el servicio para poder obtener el total de paginas.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request, page=1):
    images = []
    images = services.getAllImages()
    favourite_list = []
    favourite_list = services.getAllFavourites(request)
    total_pages = services.getAllPages()
    
    paginator = Paginator(images, per_page=20)
    page_object = paginator.get_page(page)
    
    context = {
        'page_object': page_object,
        'favourite_list': favourite_list,
        'total_pages': total_pages,
    }

    return render(request, 'home.html', context)

def search(request, page=1):
    search_msg = request.POST.get('query', '')
    if (search_msg != ''):
        images = services.getAllImages(search_msg)
        favourite_list = services.getAllFavourites(request)

        paginator = Paginator(images, per_page=20)
        page_object = paginator.get_page(page)

        context = {
            'page_object': page_object,
            'favourite_list': favourite_list
        }

        return render(request, 'home.html', context)
    else:
        return redirect('home')



# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('login')