from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def admin_required(view_func):
    """Só deixa entrar quem está logado E é administrador (staff)."""
    @wraps(view_func)
    @login_required(login_url="/admin/login/")
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def aluno_required(view_func):
    """Só deixa entrar quem está logado E tem perfil de aluno."""
    @wraps(view_func)
    @login_required(login_url="/login-aluno/")
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, "aluno"):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def instrutor_required(view_func):
    """Só deixa entrar quem está logado E tem perfil de instrutor."""
    @wraps(view_func)
    @login_required(login_url="/login-instrutor/")
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, "instrutor"):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper