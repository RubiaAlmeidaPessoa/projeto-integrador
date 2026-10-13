from django.contrib import admin
from .models import Aluno, Plano, Matricula, Pagamento, Instrutor, FichaTreino, ExercicioFicha, CheckIn, AulaColetiva, Inscricao

admin.site.site_header = "Academia FitPro"
admin.site.site_title = "Academia FitPro"
admin.site.index_title = "Painel Administrativo"

admin.site.register(Aluno)
admin.site.register(Plano)
admin.site.register(Matricula)
admin.site.register(Pagamento)
admin.site.register(Instrutor)
admin.site.register(CheckIn)

class ExercicioFichaInline(admin.TabularInline):
    model = ExercicioFicha
    extra = 1  


@admin.register(FichaTreino)
class FichaTreinoAdmin(admin.ModelAdmin):
    inlines = [ExercicioFichaInline]

class InscricaoInline(admin.TabularInline):
    model = Inscricao
    extra = 1


@admin.register(AulaColetiva)
class AulaColetivaAdmin(admin.ModelAdmin):
    inlines = [InscricaoInline]
