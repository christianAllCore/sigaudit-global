# SIGAudit Global — QA/QC de migración GIS para utilities

> Public-safe bilingual note. No client names, no private links, no internal systems, no real data.

## Español

En proyectos GIS de utilities, una migración no termina cuando los datos “ya están cargados”. Termina cuando existe evidencia verificable de que la información fuente y la geodatabase destino son consistentes, trazables y suficientemente confiables para operación, análisis y publicación.

SIGAudit Global propone una forma práctica de organizar esa validación con cuatro capas de control:

| Capa | Pregunta clave | Evidencia pública segura |
|---|---|---|
| Inventario | ¿Qué capas, tablas y hojas fueron revisadas? | Matriz de datasets, capas y campos con datos ficticios. |
| Estructura | ¿Los campos, tipos, longitudes, dominios y relaciones coinciden? | Checklist técnico y reporte de diferencias. |
| Contenido | ¿Los conteos, nulos, códigos de dominio y valores críticos son consistentes? | Reporte Excel con totales, porcentajes y alertas. |
| Trazabilidad | ¿Se puede explicar cada hallazgo y repetir la revisión? | Bitácora de ejecución, reglas y criterios de aceptación. |

La idea central es simple: convertir revisiones dispersas en un producto técnico repetible. Un buen auditor GIS no solo encuentra errores; deja un camino claro para corregirlos, explicar decisiones y demostrar calidad.

### Ejemplo de servicio digital seguro

**SIGAudit Data Quality Starter** puede empaquetarse como un producto inicial con:

- Plantilla Excel de control de migración.
- Script Python para revisar CSV ficticios.
- Checklist de estructura GIS.
- Guía corta para interpretar hallazgos.
- Reporte ejecutivo de una página.

Todo el material público debe usar datos sintéticos o generalizados. La lógica conceptual puede compartirse; los datos reales, rutas internas, credenciales, clientes y código privado no.

## English

In utility GIS projects, a migration is not finished when data is “loaded”. It is finished when there is verifiable evidence that the source information and the target geodatabase are consistent, traceable and reliable enough for operations, analysis and publication.

SIGAudit Global proposes a practical way to organize this validation through four control layers:

| Layer | Key question | Safe public evidence |
|---|---|---|
| Inventory | Which layers, tables and sheets were reviewed? | Dataset, layer and field matrix using fake data. |
| Structure | Do fields, types, lengths, domains and relationships match? | Technical checklist and difference report. |
| Content | Are counts, nulls, domain codes and critical values consistent? | Excel report with totals, percentages and alerts. |
| Traceability | Can each finding be explained and the review repeated? | Execution log, rules and acceptance criteria. |

The central idea is simple: turn scattered reviews into a repeatable technical product. A strong GIS auditor does not only find errors; they leave a clear path to correct them, explain decisions and demonstrate quality.

### Safe digital service example

**SIGAudit Data Quality Starter** can be packaged as an initial product with:

- Excel migration control template.
- Python script for checking fake CSV files.
- GIS structure checklist.
- Short guide to interpret findings.
- One-page executive report.

All public material must use synthetic or generalized data. Conceptual logic can be shared; real data, internal paths, credentials, clients and private code cannot.
