from django.contrib import admin
from .models import AuditQuestion, Audit, AuditAnswer


@admin.register(AuditQuestion)
class AuditQuestionAdmin(admin.ModelAdmin):
    list_display = ("codigo", "texto", "categoria", "activo")
    list_filter = ("categoria", "activo")
    search_fields = ("codigo", "texto")


class AuditAnswerInline(admin.TabularInline):
    model = AuditAnswer
    extra = 0


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha", "auditor", "estado")
    list_filter = ("estado", "auditor", "fecha")
    search_fields = ("objetivo", "auditor__username", "auditor__email")
    inlines = [AuditAnswerInline]


@admin.register(AuditAnswer)
class AuditAnswerAdmin(admin.ModelAdmin):
    list_display = ("auditoria", "pregunta", "respuesta")
    list_filter = ("respuesta",)
    search_fields = ("auditoria__id", "pregunta__texto")
