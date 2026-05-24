# SIGAudit Data Quality Starter

**ES:** Kit inicial público para demostrar auditoría básica de calidad de datos en flujos GIS, utilities, Excel/CSV y migraciones.  
**EN:** Public starter kit to demonstrate basic data-quality auditing for GIS, utility, Excel/CSV and migration workflows.

> Este proyecto usa únicamente datos ficticios. No contiene contraseñas, tokens, enlaces privados, datos de clientes, rutas internas, código de empleadores ni información sensible.  
> This project uses fake data only. It contains no passwords, tokens, private links, client data, internal paths, employer code or sensitive information.

---

## Español

### ¿Qué problema resuelve?

En proyectos GIS, eléctricos, catastrales o institucionales, una gran parte del riesgo aparece antes del mapa: datos incompletos, duplicados, códigos fuera de dominio, campos obligatorios vacíos, errores de migración y fuentes que no coinciden con el destino.

Este mini-proyecto muestra una forma simple de convertir archivos CSV exportados desde sistemas GIS o bases de datos en un reporte inicial de calidad.

### Qué valida esta versión inicial

- Campos obligatorios vacíos.
- Valores duplicados por clave.
- Valores fuera de dominio.
- Conteo de registros.
- Porcentaje de completitud por campo.
- Reportes CSV de hallazgos.

### Casos de uso

- Auditoría preliminar de una migración GIS.
- Revisión de activos eléctricos exportados a CSV.
- Validación de catastro, clientes, transformadores, alimentadores o inventarios.
- Demostración pública de metodología QA/QC sin exponer datos privados.

### Cómo ejecutar

```bash
pip install pandas
python src/sigaudit_basic_audit.py --data sample_data/assets.csv --rules templates/validation_rules.csv --out output
```

---

## English

### What problem does it solve?

In GIS, utility, cadastral and institutional projects, risk often starts before the map: incomplete data, duplicate keys, invalid coded values, missing required fields, migration issues and mismatches between source and target datasets.

This mini-project demonstrates a simple way to turn CSV exports from GIS systems or databases into an initial data quality report.

### What this first version checks

- Missing required fields.
- Duplicate key values.
- Values outside expected domains.
- Record counts.
- Field completeness percentage.
- CSV findings reports.

### Use cases

- Preliminary GIS migration audit.
- Electric utility asset data review.
- Validation of cadastral, customer, transformer, feeder or inventory data.
- Public QA/QC methodology demo without exposing private data.

### Run

```bash
pip install pandas
python src/sigaudit_basic_audit.py --data sample_data/assets.csv --rules templates/validation_rules.csv --out output
```

---

## Expected outputs

- `output/field_completeness.csv`
- `output/duplicate_keys.csv`
- `output/domain_violations.csv`
- `output/audit_summary.csv`

## Roadmap

- Add Excel input support.
- Add source-vs-target comparison.
- Add relationship/orphan-record checks.
- Add ArcGIS/ArcPy adapters in a separate optional module.
- Add HTML/Excel report generation.
- Add bilingual documentation.
