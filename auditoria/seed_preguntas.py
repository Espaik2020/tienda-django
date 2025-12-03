from auditoria.models import AuditQuestion

# (codigo, texto, categoría)
QUESTIONS = [
    # 4. CONTEXTO DE LA ORGANIZACIÓN
    ("4.1-1", "¿Se tienen identificadas las cuestiones internas asociadas a las necesidades de la empresa y su impacto en el SGA?", "4. CONTEXTO DE LA ORGANIZACION"),
    ("4.1-2", "¿Se tienen identificadas las cuestiones externas asociadas a las necesidades de la empresa y su impacto en el SGA?", "4. CONTEXTO DE LA ORGANIZACION"),
    ("4.2-1", "¿Existe una metodología para la identificación inicial de las partes interesadas?", "4. CONTEXTO DE LA ORGANIZACION"),
    ("4.2-2", "¿Se identifican correctamente los requisitos de las partes interesadas para el desarrollo del SGA?", "4. CONTEXTO DE LA ORGANIZACION"),
    ("4.3-1", "¿El alcance del SGA es acorde a las metas y objetivos propuestos según las necesidades de la organización?", "4. CONTEXTO DE LA ORGANIZACION"),
    ("4.4-1", "¿El SGA interrelaciona todos los procesos necesarios para una correcta interpretación?", "4. CONTEXTO DE LA ORGANIZACION"),

    # 5. LIDERAZGO
    ("5.1-1", "¿La alta dirección está comprometida con el SGA para que sea una herramienta eficaz?", "5. LIDERAZGO"),
    ("5.1-2", "¿Los objetivos planteados por la empresa están acordes a sus necesidades?", "5. LIDERAZGO"),
    ("5.1-3", "¿Se facilitan los recursos necesarios para la implementación del SGA?", "5. LIDERAZGO"),
    ("5.1-4", "¿La alta dirección dirige y apoya a toda la planta de trabajadores para lograr una gestión eficaz y la mejora continua?", "5. LIDERAZGO"),
    ("5.2-1", "¿La empresa tiene establecida una política ambiental acorde a sus necesidades?", "5. LIDERAZGO"),
    ("5.2-2", "¿La política ambiental de la empresa tiene soportes teóricos que respalden los objetivos del SGA?", "5. LIDERAZGO"),
    ("5.2-3", "¿La política ambiental de la empresa genera compromisos de cumplimiento con sus empleados?", "5. LIDERAZGO"),
    ("5.3-1", "¿La alta dirección ha generado canales efectivos de comunicación para el desarrollo y evolución del SGA?", "5. LIDERAZGO"),

    # 6. PLANIFICACIÓN
    ("6.1.1-1", "¿La empresa ha generado indicadores ambientales que permitan reportes positivos y negativos para facilitar acciones correctivas?", "6. PLANIFICACIÓN"),
    ("6.1.1-2", "¿La empresa ha identificado previamente riesgos y oportunidades y les ha dado tratamiento para asegurar un SGA viable?", "6. PLANIFICACIÓN"),
    ("6.1.1-3", "¿Se cuenta con información documentada, organizada por procesos y de fácil acceso para actuar ante situaciones imprevistas?", "6. PLANIFICACIÓN"),
    ("6.1.1-4", "¿Se tienen identificadas las situaciones que pueden generar incidentes, accidentes o impactos ambientales en la zona de incidencia?", "6. PLANIFICACIÓN"),
    ("6.1.1-5", "¿Se cuenta con la documentación necesaria para la definición del alcance del sistema de gestión ambiental?", "6. PLANIFICACIÓN"),

    ("6.1.2-1", "¿Cuenta la empresa con la metodología adecuada para la identificación de sus aspectos ambientales?", "6. PLANIFICACIÓN"),
    ("6.1.2-2", "¿Se han implementado acciones preventivas y correctivas asociadas con aire, agua y suelo para mitigar impactos ambientales?", "6. PLANIFICACIÓN"),
    ("6.1.2-3", "¿La identificación de los aspectos ambientales ha sido comunicada en todos los niveles de la empresa?", "6. PLANIFICACIÓN"),
    ("6.1.2-4", "¿Se cuenta con información documentada donde los aspectos e impactos ambientales están plenamente identificados y clasificados según su incidencia?", "6. PLANIFICACIÓN"),

    ("6.1.3-1", "¿La organización tiene identificadas sus obligaciones respecto a los impactos ambientales que provoca?", "6. PLANIFICACIÓN"),
    ("6.1.3-2", "¿Cuenta con procedimientos para la identificación y aplicación de los requisitos legales ambientales aplicables a su producción?", "6. PLANIFICACIÓN"),
    ("6.1.3-3", "¿Se cuenta con información documentada y ordenada sobre los requisitos legales y otros requisitos ambientales?", "6. PLANIFICACIÓN"),

    ("6.1.4-1", "¿Cuenta la empresa con la implementación y mantenimiento de un plan de acción para el cumplimiento de objetivos y metas ambientales?", "6. PLANIFICACIÓN"),

    # 7. APOYO
    ("7.1-1", "¿La empresa facilita los recursos suficientes para la implementación, mantenimiento y mejora continua del SGA?", "7. APOYO"),

    ("7.2-1", "¿Cuenta con personal competente para la realización de las actividades productivas?", "7. APOYO"),
    ("7.2-2", "¿Se dispone de información documentada que evidencia las competencias requeridas según la ISO 14001:2015?", "7. APOYO"),
    ("7.2-3", "¿La empresa ha evaluado la eficacia de las medidas tomadas para asegurar la competencia del personal?", "7. APOYO"),

    ("7.3-1", "¿Todo el personal conoce la política ambiental, los objetivos y cómo su aporte influye en el desempeño del SGA?", "7. APOYO"),
    ("7.3-2", "¿Se han identificado las necesidades de formación relacionadas con los aspectos ambientales y el SGA?", "7. APOYO"),
    ("7.3-3", "¿Cuenta la empresa con procedimientos necesarios para generar conciencia en los empleados respecto al sistema de gestión ambiental?", "7. APOYO"),

    ("7.4.1-1", "¿Los procesos de comunicación interna y externa son efectivos para el cumplimiento del SGA?", "7. APOYO"),
    ("7.4.2-1", "¿Cuenta la empresa con recepción, documentación y respuesta a las comunicaciones pertinentes de las partes interesadas externas?", "7. APOYO"),
    ("7.4.3-1", "¿Cuenta con procedimientos para la comunicación interna entre los distintos niveles y funciones de la organización?", "7. APOYO"),

    ("7.5-1", "¿Cuenta con la descripción de los elementos principales del sistema de gestión ambiental y su interacción?", "7. APOYO"),
    ("7.5-2", "¿Cuenta con la descripción del alcance del sistema de gestión ambiental?", "7. APOYO"),
    ("7.5-3", "¿Cuenta con documentos y registros revisados y aprobados requeridos por la norma y por la organización?", "7. APOYO"),
    ("7.5-4", "¿Cuenta con los documentos de control requeridos por el SGA y por la norma ISO 14001:2015?", "7. APOYO"),
    ("7.5-5", "¿La información está disponible, adecuadamente protegida, correctamente almacenada y lista para su uso autorizado?", "7. APOYO"),

    # 8. OPERACIÓN
    ("8.1-1", "¿Hay control de los requisitos ambientales en relación con el ciclo de vida de los productos y sus impactos ambientales?", "8. OPERACIÓN"),
    ("8.1-2", "¿Cuenta con procedimientos documentados para controlar situaciones con aspectos ambientales significativos en transporte, entrega y disposición final?", "8. OPERACIÓN"),

    ("8.2-1", "¿Cuenta con procedimientos necesarios para la identificación de situaciones potenciales de emergencia?", "8. OPERACIÓN"),
    ("8.2-2", "¿Se revisan periódicamente y modifican los procedimientos de emergencia, en particular después de presentarse emergencias reales?", "8. OPERACIÓN"),
    ("8.2-3", "¿Se realizan pruebas periódicas de los procedimientos de emergencia?", "8. OPERACIÓN"),
    ("8.2-4", "¿La empresa cuenta con información documentada que evidencia una buena gestión y atención ante emergencias?", "8. OPERACIÓN"),

    # 9. EVALUACIÓN DEL DESEMPEÑO
    ("9.1.1-1", "¿Está identificado todo lo que necesita ser monitoreado y medido, así como los métodos y cronograma de seguimiento?", "9. EVALUACIÓN DEL DESEMPEÑO"),
    ("9.1.1-2", "¿Cuenta con registros de seguimiento y medición de los equipos usados para asegurar que se mantengan calibrados o verificados?", "9. EVALUACIÓN DEL DESEMPEÑO"),
    ("9.1.1-3", "¿Se cuenta con información documentada sobre la medición, análisis y evaluación de resultados como evidencia del seguimiento?", "9. EVALUACIÓN DEL DESEMPEÑO"),

    ("9.1.2-1", "¿Cuenta con procedimientos para evaluar periódicamente el cumplimiento de los requisitos legales ambientales aplicables?", "9. EVALUACIÓN DEL DESEMPEÑO"),
    ("9.1.2-2", "¿Cuenta con registros de los resultados de las evaluaciones periódicas de cumplimiento?", "9. EVALUACIÓN DEL DESEMPEÑO"),
    ("9.1.2-3", "¿Se evalúan estos registros para apoyar la toma de decisiones en pro del ambiente?", "9. EVALUACIÓN DEL DESEMPEÑO"),

    ("9.2.2-1", "¿Cuenta con auditorías internas periódicas para la evaluación del sistema de gestión ambiental?", "9. EVALUACIÓN DEL DESEMPEÑO"),
    ("9.2.2-2", "¿Cuenta con un programa de auditorías que considera la importancia ambiental de las operaciones y los resultados de auditorías previas?", "9. EVALUACIÓN DEL DESEMPEÑO"),

    ("9.3-1", "¿Ha sido planificada la revisión del SGA para asegurar su conveniencia, adecuación y eficacia continua?", "9. EVALUACIÓN DEL DESEMPEÑO"),
    ("9.3-2", "¿Los resultados de la evaluación de la auditoría han sido útiles para implementar mejoras continuas?", "9. EVALUACIÓN DEL DESEMPEÑO"),
    ("9.3-3", "¿Existe información documentada como evidencia de la revisión del SGA por la alta dirección?", "9. EVALUACIÓN DEL DESEMPEÑO"),

    # 10. MEJORA
    ("10-1", "¿Se han implementado acciones de mejora para que el SGA logre sus metas y objetivos planteados?", "10. MEJORA"),
    ("10-2", "¿Cuenta con procedimientos para tratar no conformidades reales y potenciales y tomar las acciones correctivas y preventivas necesarias?", "10. MEJORA"),
    ("10-3", "¿La organización utiliza sus falencias para mejorar y fortalecer sus procesos?", "10. MEJORA"),
]


def run():
    creadas = 0
    for codigo, texto, categoria in QUESTIONS:
        obj, created = AuditQuestion.objects.update_or_create(
            codigo=codigo,
            defaults={
                "texto": texto,
                "categoria": categoria,
                "activo": True,
            },
        )
        if created:
            creadas += 1
    print(f"Preguntas procesadas: {len(QUESTIONS)}  |  Nuevas creadas: {creadas}")


# Cuando se usa `python manage.py shell < auditoria/seed_preguntas.py`
# Django ejecuta el archivo completo, así que llamamos a run():
if __name__ == "__main__":
    run()
else:
    # Si se importa dentro del shell, se puede llamar manualmente:
    run()
