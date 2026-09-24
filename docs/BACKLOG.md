# Backlog wdrożenia

## M0 — obecny szkielet

- API, modele domenowe, rejestr skillsów, pipeline, linter i testy.
- Jawne zaślepki zamiast pozornych wyników AI.

## M1 — użyteczny pilot

- adapter do jednego zatwierdzonego LLM;
- trwały store (PostgreSQL) i wersjonowanie artefaktów;
- UI review/approve/reject;
- import notatek i dokumentów;
- eksport do Jira/Confluence;
- telemetryka jakości, kosztu i czasu.

## M2 — banking IP

- katalog NFR banku;
- ekstrakcja reguł biznesowych;
- wymagania danych, lineage i quality rules;
- obligation extraction z cytowaniem fragmentów;
- model approval gates dla Compliance/Risk/Security/Architecture.

## M3 — graph i impact

- graf Regulation → Obligation → Rule → BR → FR → System/API/Data → Test → Evidence;
- wykrywanie konfliktów i duplikatów;
- impact analysis ze stopniem pewności i wyjaśnieniem ścieżek.

## Kryteria pilota

Porównać z dwoma zakończonymi inicjatywami: czas na wymaganie, liczbę iteracji review, kompletność traceability, czas impact analysis, defekty wymagań i rework po development.

