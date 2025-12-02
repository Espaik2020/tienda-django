from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditQuestion(models.Model):
    """Preguntas estándar de la auditoría (catálogo de preguntas)."""
    codigo = models.CharField("Código", max_length=20, unique=True)
    texto = models.CharField("Pregunta", max_length=255)
    categoria = models.CharField("Categoría", max_length=100, blank=True)
    activo = models.BooleanField("Activa", default=True)

    class Meta:
        verbose_name = "Pregunta de auditoría"
        verbose_name_plural = "Preguntas de auditoría"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.texto[:40]}"


class Audit(models.Model):
    """Encabezado de una auditoría (una ejecución)."""
    ESTADO_CHOICES = [
        ("EN_PROCESO", "En proceso"),
        ("CERRADA", "Cerrada"),
    ]

    fecha = models.DateTimeField("Fecha", auto_now_add=True)
    auditor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="auditorias",
        verbose_name="Auditor",
    )
    objetivo = models.CharField(
        "Objetivo / Alcance",
        max_length=200,
        blank=True,
    )
    estado = models.CharField(
        "Estado",
        max_length=20,
        choices=ESTADO_CHOICES,
        default="EN_PROCESO",
    )
    observaciones_generales = models.TextField(
        "Observaciones generales",
        blank=True,
    )

    class Meta:
        verbose_name = "Auditoría"
        verbose_name_plural = "Auditorías"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Auditoría #{self.id} - {self.fecha:%Y-%m-%d}"


class AuditAnswer(models.Model):
    """Respuesta a cada pregunta dentro de una auditoría."""
    RESP_CHOICES = [
        ("C", "Cumple"),
        ("NC", "No cumple"),
        ("NA", "No aplica"),
    ]

    auditoria = models.ForeignKey(
        Audit,
        on_delete=models.CASCADE,
        related_name="respuestas",
        verbose_name="Auditoría",
    )
    pregunta = models.ForeignKey(
        AuditQuestion,
        on_delete=models.PROTECT,
        verbose_name="Pregunta",
    )
    respuesta = models.CharField(
        "Respuesta",
        max_length=2,
        choices=RESP_CHOICES,
    )
    comentario = models.TextField("Comentario", blank=True)

    class Meta:
        verbose_name = "Respuesta de auditoría"
        verbose_name_plural = "Respuestas de auditoría"
        unique_together = ("auditoria", "pregunta")

    def __str__(self):
        return f"{self.auditoria_id} - {self.pregunta.codigo}"
