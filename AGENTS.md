# Instructions pour ChatGPT Work et Codex — MNIN NBDA

## Autorité documentaire
1. Dernières validations explicites du propriétaire sur la maquette et les fonctionnalités.
2. docs/references/PROMPT_MASTER_HOME_DESKTOP_XL_2026-10-11.md pour les éléments de home qu'il précise.
3. docs/references/PROMPT_MASTER_WORDPRESS_V4_2.md pour l'architecture générale.
4. Le code vérifié sur le site WordPress existant, après audit en lecture seule.
En cas de conflit, documenter le point dans docs/STATUS.md et ne jamais inventer une décision. La référence visuelle complète n'est pas stockée ici : ne pas prétendre reproduire pixel à pixel un visuel inaccessible.

## Organisation des quatre rôles
- Agent 01 Pilotage (agents/01-pilotage.md) : objectifs, planification et arbitrage des contradictions.
- Agent 02 Développement (agents/02-developpement.md) : code WordPress maintenable et testé.
- Agent 03 Qualité (agents/03-qualite.md) : contrôle indépendant UX/RTL/accessibilité/sécurité.
- Agent 04 Intégration (agents/04-integration.md) : contrôle de version, CI, versions ZIP, déploiement après accord.
Les rôles sont des instructions exploitables par Work et Codex, non quatre services IA hébergés en permanence.

## Méthode
- Commencer par le P0 : inventorier WordPress actuel, thème MNIN NBDA V4 et limites des accès ; ne jamais écraser l'existant.
- Priorité P1 : accueil haute fidélité desktop + mobile FR/AR, validation client avant autres pages.
- Respecter la séparation mnin-nbda-theme / mnin-nbda-core.
- Utiliser WordPress natif et bibliothèques open source, sans API payante.
- Préférer une branche de travail par tâche, modifications petites, commits descriptifs, contrôle de risques.
- Avant de coder : critères d'acceptation et fichiers concernés. Après : preuves, résultats tests, limites, statut.
- CI n'est pas un agent IA ; elle n'écrit pas de code ni ne lance de déploiement automatique.
- Les données réelles des élèves et parents sont sensibles : pas d'export, pas de faux accès, pas de données personnelles en logs.
- Aucun déploiement WordPress, changement de plugin actif, paiement ni activation publique sans accord explicite.
- Ne jamais affirmer 24h/24 autonome sans scheduler concret et vérification des exécutions.
- Statuts de test autorisés : PASS, FAIL, NON TESTÉ, BLOQUÉ.

## Définition de terminé
Livrable réellement construit, tests exécutés documentés, absence d'anomalie bloquante, conformité vérifiée, validation explicite du propriétaire pour déploiement.
