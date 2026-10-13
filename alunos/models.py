from django.db import models
from django.contrib.auth.models import User


class Plano(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    duracao_meses = models.PositiveIntegerField()

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    data_cadastro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nome

    @property
    def plano_atual(self):
        matricula = self.matricula_set.filter(ativa=True).first()
        return matricula.plano if matricula else None


class Instrutor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    especialidade = models.CharField(max_length=100, help_text="Ex: Musculação, Funcional, Natação")

    def __str__(self):
        return self.nome


class Matricula(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    plano = models.ForeignKey(Plano, on_delete=models.PROTECT)
    data_inicio = models.DateField()
    data_vencimento = models.DateField()
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.aluno} - {self.plano}"


class Pagamento(models.Model):
    STATUS_CHOICES = [
        ("PAGO", "Pago"),
        ("PENDENTE", "Pendente"),
        ("ATRASADO", "Atrasado"),
    ]
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="PENDENTE")

    def __str__(self):
        return f"{self.matricula.aluno} - R${self.valor}"


class FichaTreino(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="fichas")
    instrutor = models.ForeignKey(Instrutor, on_delete=models.SET_NULL, null=True)
    objetivo = models.CharField(max_length=100, blank=True)
    criada_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Ficha de {self.aluno} ({self.criada_em})"


class ExercicioFicha(models.Model):
    ficha = models.ForeignKey(FichaTreino, on_delete=models.CASCADE, related_name="exercicios")
    nome = models.CharField(max_length=100)
    series = models.PositiveIntegerField(default=3)
    repeticoes = models.PositiveIntegerField(default=12)

    def __str__(self):
        return self.nome


class CheckIn(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="checkins")
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno} - {self.data_hora:%d/%m/%Y %H:%M}"


class AulaColetiva(models.Model):
    DIAS_SEMANA = [
        ("SEG", "Segunda"), ("TER", "Terça"), ("QUA", "Quarta"),
        ("QUI", "Quinta"), ("SEX", "Sexta"), ("SAB", "Sábado"), ("DOM", "Domingo"),
    ]
    nome = models.CharField(max_length=100, help_text="Ex: Spinning, Yoga, Funcional")
    instrutor = models.ForeignKey(Instrutor, on_delete=models.SET_NULL, null=True)
    dia_semana = models.CharField(max_length=10, choices=DIAS_SEMANA)
    horario = models.TimeField()
    vagas = models.PositiveIntegerField(default=20)

    def __str__(self):
        return f"{self.nome} - {self.get_dia_semana_display()} {self.horario}"


class Inscricao(models.Model):
    aula = models.ForeignKey(AulaColetiva, on_delete=models.CASCADE, related_name="inscricoes")
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("aula", "aluno")

    def __str__(self):
        return f"{self.aluno} em {self.aula}"