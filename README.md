# MNIN NBDA — Référentiel des huit experts IA

Dépôt de coordination ChatGPT Work / Codex / GitHub pour le projet WordPress MNIN NBDA. **Huit rôles sont configurés en Markdown, mais aucun service IA permanent n'est lancé par leur seule création.**

## Commencer
1. Lire docs/WORK_MASTER_START.md dans ChatGPT Work avec l'accès au dépôt GitHub.
2. Confier la première mission au DSI : audit **sans écriture** du site WordPress MNIN NBDA V4 et préparation du backlog.
3. Répartir les travaux uniquement entre les rôles pertinents.
4. Versionner les changements, tester, documenter et obtenir l'accord avant déploiement.

## Fichiers centraux
- AGENTS.md : règles communes.
- agents/manifest.json : inventaire formel des huit rôles.
- agents/01-directeur-si.md à agents/08-devops.md : prompts spécialisés.
- docs/AGENT_OPERATING_MODEL.md : orchestration, handoffs, portes de validation.
- docs/WORK_MASTER_START.md : prompt maître de démarrage dans Work.
- docs/ROADMAP.md, docs/STATUS.md : phases et état vérifié.
- docs/references/PROMPT_MASTER_WORDPRESS_V4_2.md : cahier directeur.
- docs/references/PROMPT_MASTER_HOME_DESKTOP_XL_2026-10-11.md : référence textuelle de Home.
- scripts/validate_workspace.py : contrôles déterministes locaux.
- .github/workflows/validation.yml : CI sans clé API IA.

## Architecture cible
WordPress personnalisé : mnin-nbda-theme (design) + mnin-nbda-core (pédagogie). Éviter Tutor LMS / Elementor obligatoires, préserver FR/AR et RTL, aucune dépendance externe payante nécessaire aux fonctions essentielles.

## Sécurité et limites
Le site WordPress existant est en staging. Aucun écrasement, installation, activation d'extension ou mise en production n'est autorisé automatiquement. Aucune API IA payante n'est configurée. Les quotas GitHub Actions et les fonctionnalités Work/Codex dépendent du compte et de l'offre accessibles ; **une exécution 24 h/24 non-stop n'est pas mise en place ici**.
