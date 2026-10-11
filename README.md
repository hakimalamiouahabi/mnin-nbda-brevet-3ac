# MNIN NBDA — développement WordPress

Référentiel du projet éducatif marocain MNIN NBDA. État initial : **orchestration préparée, agents non autonomes tant que les exécutions Work/Codex ne sont pas configurées**.

## Références
- docs/references/PROMPT_MASTER_WORDPRESS_V4_2.md : spécifications métier et techniques V4.2.
- docs/references/PROMPT_MASTER_HOME_DESKTOP_XL_2026-10-11.md : dernière référence textuelle responsive de l'accueil.
- AGENTS.md : règles transversales de travail.
- agents/ : quatre rôles spécialisés à utiliser dans ChatGPT Work / Codex.
- docs/WORK_MASTER_START.md : instruction de démarrage dans Work.
- docs/ROADMAP.md : étapes, dépendances et recette.
- docs/STATUS.md : situation réelle et points en attente.

## Contraintes invariantes
- Aucune clé ni abonnement à une API IA payante.
- Pas de nouveau coût logiciel obligatoire ; aucune opération susceptible de facturation sans autorisation.
- Aucune modification du WordPress existant avant approbation explicite de la livraison.
- Site WordPress.com déjà existant (staging) : ne pas substituer ce dépôt à ses fichiers sans sauvegarde/audit.
- Respect intégral de la dernière maquette validée : priorité à l'accueil, aucun bloc de matières sur l'accueil.
- Thème personnalisé et extension métier mnin-nbda-core ; pas de Tutor LMS / Elementor obligatoire.
- Langues FR/AR et RTL ; Polylang Free facultatif, activation conditionnée à un test.
- Protection des données des mineurs et séparation stricte des données des foyers.
- Aucun test non réalisé ne doit être déclaré réussi.

## Démarrage
Dans Work : ouvrir le dépôt autorisé, lire AGENTS.md, docs/WORK_MASTER_START.md et les deux prompts masters ; procéder à l'audit non destructif puis produire les premières tâches. Les fichiers agents/ sont des consignes de rôle, pas des processus automatiquement activés.
