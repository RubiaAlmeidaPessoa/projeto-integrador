from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .decorators import admin_required, aluno_required, instrutor_required
from .models import (
    Aluno, Plano, Pagamento, Instrutor, FichaTreino, ExercicioFicha,
    CheckIn, AulaColetiva, Inscricao,
)


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("lista_alunos")
        if hasattr(request.user, "aluno"):
            return redirect("minha_ficha")
    return render(request, "alunos/home.html")


# ---------- ADMINISTRADOR ----------

@admin_required
def lista_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, "alunos/lista_alunos.html", {"alunos": alunos})


@admin_required
def lista_planos(request):
    planos = Plano.objects.all()
    return render(request, "alunos/lista_planos.html", {"planos": planos})


@admin_required
def lista_pagamentos(request):
    pagamentos = Pagamento.objects.select_related("matricula__aluno").all()
    return render(request, "alunos/lista_pagamentos.html", {"pagamentos": pagamentos})


@admin_required
def lista_instrutores(request):
    instrutores = Instrutor.objects.all()
    return render(request, "alunos/lista_instrutores.html", {"instrutores": instrutores})


@admin_required
def lista_fichas(request):
    fichas = FichaTreino.objects.select_related("aluno", "instrutor").prefetch_related("exercicios").all()
    return render(request, "alunos/lista_fichas.html", {"fichas": fichas})


@admin_required
def lista_checkins(request):
    checkins = CheckIn.objects.select_related("aluno").order_by("-data_hora")[:50]
    return render(request, "alunos/lista_checkins.html", {"checkins": checkins})


@admin_required
def lista_aulas(request):
    aulas = AulaColetiva.objects.select_related("instrutor").prefetch_related("inscricoes__aluno").all()
    return render(request, "alunos/lista_aulas.html", {"aulas": aulas})


# ---------- ALUNO ----------

def aluno_login(request):
    if request.method == "POST":
        usuario = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )
        if usuario is not None:
            login(request, usuario)
            return redirect("minha_ficha")
        return render(request, "alunos/aluno_login.html", {"erro": "Usuário ou senha inválidos."})
    return render(request, "alunos/aluno_login.html")


def aluno_logout(request):
    logout(request)
    return redirect("aluno_login")


@aluno_required
def minha_ficha(request):
    fichas = request.user.aluno.fichas.all()
    return render(request, "alunos/minha_ficha.html", {"fichas": fichas})


@aluno_required
@require_POST
def fazer_checkin(request):
    CheckIn.objects.create(aluno=request.user.aluno)
    return redirect("minha_ficha")


@aluno_required
def aulas_disponiveis(request):
    aulas = AulaColetiva.objects.select_related("instrutor").prefetch_related("inscricoes").all()
    minhas_inscricoes = set(
        Inscricao.objects.filter(aluno=request.user.aluno).values_list("aula_id", flat=True)
    )
    return render(request, "alunos/aulas_disponiveis.html", {
        "aulas": aulas,
        "minhas_inscricoes": minhas_inscricoes,
    })


@aluno_required
@require_POST
def inscrever_aula(request, aula_id):
    aula = get_object_or_404(AulaColetiva, id=aula_id)
    if aula.inscricoes.count() < aula.vagas:
        Inscricao.objects.get_or_create(aula=aula, aluno=request.user.aluno)
    return redirect("aulas_disponiveis")


@aluno_required
def meu_pagamento(request):
    pagamentos = Pagamento.objects.filter(
        matricula__aluno=request.user.aluno
    ).order_by("-data_vencimento")
    return render(request, "alunos/meu_pagamento.html", {"pagamentos": pagamentos})