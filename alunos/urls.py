from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # administrador
    path("alunos/", views.lista_alunos, name="lista_alunos"),
    path("planos/", views.lista_planos, name="lista_planos"),
    path("pagamentos/", views.lista_pagamentos, name="lista_pagamentos"),
    path("instrutores/", views.lista_instrutores, name="lista_instrutores"),
    path("fichas-treino/", views.lista_fichas, name="lista_fichas"),
    path("checkins/", views.lista_checkins, name="lista_checkins"),
    path("aulas/", views.lista_aulas, name="lista_aulas"),

    # aluno
    path("login-aluno/", views.aluno_login, name="aluno_login"),
    path("logout-aluno/", views.aluno_logout, name="aluno_logout"),
    path("minha-ficha/", views.minha_ficha, name="minha_ficha"),
    path("fazer-checkin/", views.fazer_checkin, name="fazer_checkin"),
    path("aulas-disponiveis/", views.aulas_disponiveis, name="aulas_disponiveis"),
    path("inscrever-aula/<int:aula_id>/", views.inscrever_aula, name="inscrever_aula"),
    path("meu-pagamento/", views.meu_pagamento, name="meu_pagamento"),

]