"""Generate public-safe footprint drafts for manual review.

This script intentionally creates reviewable draft files only.
It does not publish to social networks, does not contact external platforms,
and does not require private project data.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - Python < 3.9 fallback, not expected in Actions
    ZoneInfo = None  # type: ignore


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIRS = {
    "docs": REPO_ROOT / "docs",
    "posts": REPO_ROOT / "posts",
    "social": REPO_ROOT / "social",
    "products": REPO_ROOT / "products",
    "portfolio": REPO_ROOT / "portfolio",
    "state": REPO_ROOT / "automation" / "state",
}


@dataclass(frozen=True)
class DraftFile:
    path: Path
    content: str


def now_ecuador() -> datetime:
    if ZoneInfo is not None:
        return datetime.now(ZoneInfo("America/Guayaquil"))
    return datetime.now(timezone.utc)


def slug_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def display_datetime(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M Ecuador")


def split_blocked_terms(raw: str) -> List[str]:
    terms = []
    for item in re.split(r"[\n,;|]+", raw or ""):
        clean = item.strip().lower()
        if len(clean) >= 3:
            terms.append(clean)
    return sorted(set(terms))


def assert_public_safe(files: Iterable[DraftFile], blocked_terms: List[str]) -> None:
    if not blocked_terms:
        return

    violations: Dict[str, List[str]] = {}
    for draft in files:
        text = draft.content.lower()
        hits = [term for term in blocked_terms if term and term in text]
        if hits:
            violations[str(draft.path.relative_to(REPO_ROOT))] = hits[:10]

    if violations:
        formatted = json.dumps(violations, indent=2, ensure_ascii=False)
        raise RuntimeError(
            "Blocked public-footprint terms were detected. "
            "Review FOOTPRINT_BLOCKED_TERMS or the generated draft content.\n"
            f"{formatted}"
        )


def build_files(dt: datetime) -> List[DraftFile]:
    stamp = display_datetime(dt)
    date_slug = slug_date(dt)

    docs_review = f"""# Public-safe footprint review log

Generated: {stamp}

## Scope

This package is a manual-review draft for a public technical portfolio around GIS, ArcGIS, data quality, automation, technical documentation and utility data validation.

## Safety boundary

Use fake data only. Keep all private environments, internal links, confidential names, unpublished research details and sensitive identifiers out of public material.

## Review checklist

| Check | Status |
|---|---|
| Uses only generic examples | Pending manual review |
| No private infrastructure details | Pending manual review |
| No real operational data | Pending manual review |
| No confidential code | Pending manual review |
| Ready for manual editing | Pending manual review |

## Suggested next manual action

Open the generated files, edit them if needed, and publish manually only after review.
"""

    linkedin_es = f"""# Borrador LinkedIn — Español

Fecha: {stamp}

En proyectos GIS, la calidad de datos no se demuestra solo con mapas bonitos. Se demuestra cuando una migración puede auditarse: campos completos, dominios consistentes, relaciones válidas, geometrías revisadas y reportes que expliquen claramente qué cambió.

Estoy construyendo un laboratorio público y seguro para documentar prácticas de auditoría GIS, automatización y control de calidad usando ejemplos ficticios.

La idea es simple: convertir experiencia técnica en conocimiento reutilizable, sin exponer información sensible.

#GIS #ArcGIS #DataQuality #Automation #Utilities #Python
"""

    linkedin_en = f"""# LinkedIn draft — English

Date: {stamp}

In GIS projects, data quality is not proven only with beautiful maps. It is proven when a migration can be audited: complete fields, consistent domains, valid relationships, reviewed geometries and reports that clearly explain what changed.

I am building a public-safe portfolio lab to document GIS auditing, automation and quality-control practices using fictional examples only.

The idea is simple: turn technical experience into reusable knowledge without exposing sensitive information.

#GIS #ArcGIS #DataQuality #Automation #Utilities #Python
"""

    website_section = f"""# SIGAudit Global — public-safe service note

Generated: {stamp}

## Español

SIGAudit Global es una propuesta de servicio para auditoría de calidad de datos GIS y revisión de migraciones geoespaciales. El enfoque público se basa en ejemplos ficticios, validaciones reproducibles y documentación clara para equipos técnicos.

Servicios demostrables en portafolio:

| Área | Entregable público seguro |
|---|---|
| Inventario de campos | Plantillas con datos ficticios |
| Revisión de dominios | Reportes de consistencia |
| Control de nulos | Tablas de hallazgos |
| QA/QC de migración | Checklist técnico |
| Documentación | Guías y bitácoras de revisión |

## English

SIGAudit Global is a service concept for GIS data-quality auditing and geospatial migration review. The public footprint uses fictional examples, reproducible validations and clear documentation for technical teams.
"""

    product_note = f"""# Digital product idea — GIS Migration QA Starter Kit

Generated: {stamp}

## Product concept

A small downloadable starter kit for GIS migration QA/QC using fictional CSV samples, validation checklists and report templates.

## Included assets

| Asset | Purpose |
|---|---|
| Sample CSV files | Practice validation without real data |
| QA checklist | Guide structured review |
| Report template | Summarize findings clearly |
| README | Explain usage and limits |

## Review status

Manual review required before publishing.
"""

    portfolio_readme = f"""# Portfolio draft — SIGAudit Global

Generated: {stamp}

## Public purpose

This repository is a safe public lab for GIS data-quality auditing, migration QA/QC, utility data validation, Python automation and technical documentation.

## Current draft package

| Folder | Content |
|---|---|
| docs | Review log and documentation notes |
| posts | LinkedIn-style drafts |
| social | Short social copy |
| products | Digital product concepts |
| portfolio | Portfolio README drafts |

## Manual publication rule

Generated material is a draft. Review, edit and publish manually only after confirming it contains no sensitive information.
"""

    short_social_es = f"""# Post corto — Español

La auditoría GIS convierte una migración de datos en algo verificable: campos, dominios, geometrías, relaciones y reportes claros. Ese es el tipo de evidencia técnica que quiero mostrar en mi portafolio público con ejemplos ficticios.
"""

    short_social_en = f"""# Short post — English

GIS auditing turns a data migration into something verifiable: fields, domains, geometries, relationships and clear reports. That is the kind of technical evidence I want to show in my public portfolio using fictional examples.
"""

    state = {
        "generated_at_ecuador": stamp,
        "mode": "manual_review_only",
        "outputs": [
            "docs/footprint_public_safe_review.md",
            f"posts/{date_slug}_linkedin_es.md",
            f"posts/{date_slug}_linkedin_en.md",
            "social/short_post_es.md",
            "social/short_post_en.md",
            "products/gis_migration_qa_starter_kit.md",
            "portfolio/portfolio_draft.md",
        ],
    }

    return [
        DraftFile(OUTPUT_DIRS["docs"] / "footprint_public_safe_review.md", docs_review),
        DraftFile(OUTPUT_DIRS["posts"] / f"{date_slug}_linkedin_es.md", linkedin_es),
        DraftFile(OUTPUT_DIRS["posts"] / f"{date_slug}_linkedin_en.md", linkedin_en),
        DraftFile(OUTPUT_DIRS["social"] / "short_post_es.md", short_social_es),
        DraftFile(OUTPUT_DIRS["social"] / "short_post_en.md", short_social_en),
        DraftFile(OUTPUT_DIRS["products"] / "gis_migration_qa_starter_kit.md", product_note),
        DraftFile(OUTPUT_DIRS["portfolio"] / "portfolio_draft.md", portfolio_readme),
        DraftFile(OUTPUT_DIRS["state"] / "last_run.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n"),
    ]


def write_files(files: Iterable[DraftFile]) -> None:
    for directory in OUTPUT_DIRS.values():
        directory.mkdir(parents=True, exist_ok=True)

    for draft in files:
        draft.path.parent.mkdir(parents=True, exist_ok=True)
        draft.path.write_text(draft.content, encoding="utf-8")
        print(f"Generated {draft.path.relative_to(REPO_ROOT)}")


def main() -> None:
    dt = now_ecuador()
    files = build_files(dt)
    blocked_terms = split_blocked_terms(os.environ.get("FOOTPRINT_BLOCKED_TERMS", ""))
    assert_public_safe(files, blocked_terms)
    write_files(files)
    print("Public-safe draft package generated for manual review only.")


if __name__ == "__main__":
    main()
