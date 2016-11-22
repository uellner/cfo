from .utils import set_current_user


class CurrentUserMiddleware:
    """
        Classe middleware utilizada para obter o usuário que fez o request.
    """
    def process_request(self, request):
        set_current_user(getattr(request, 'user', None))
