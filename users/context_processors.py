from neapp.utils import menu

#61. Контекстный процессор для передачи Главного меню сайта во все шаблоны:
def get_neapp_context(request):
    return {'mainmenu': menu}