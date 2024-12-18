# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..transport import transport
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages(input=None):
    
    json_collection = []
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = transport.getAllImages(input)
    
    # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
    images = []
    for img in json_collection:
        card = translator.fromRequestIntoCard(img)
        images.append(card)

    return images

def getAllPages(input=None):
    pages = 0
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    pages = transport.getAllPages(input)
    return pages

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = translator.fromTemplateIntoCard(request) # transformamos un request del template en una Card.
    fav.user = get_user(request) # le asignamos el usuario correspondiente.
    return repositories.saveFavourite(fav) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)
        
        favourite_list = []
        # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        favourite_list = repositories.getAllFavourites(user)
        mapped_favourites = []

        for favourite in favourite_list:
            card = ''
            card = translator.fromRepositoryIntoCard(favourite)# transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)
        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.