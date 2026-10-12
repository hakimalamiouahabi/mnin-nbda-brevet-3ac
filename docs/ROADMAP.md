# Roadmap opérationnelle — MNIN NBDA, orchestrée par huit experts

## P0 — Audit et reprise sécurisée (DSI + DevOps + Web + Design)
- [ ] Auditer WordPress.com existant et thème actif MNIN NBDA V4 en lecture seule.
- [ ] Identifier source, contenu, version, sauvegarde/restauration et accès autorisés.
- [ ] Vérifier visuel original de la maquette Home et périmètre 3AC / 1AC–3AC.
- [ ] DSI : produire backlog priorisé et registre de décisions.
- [ ] DevOps : confirmer le fonctionnement de la CI et ses quotas ; ne déployer aucun code.

## P1 — Home validée (Design + Web + DevOps + DSI)
- [ ] Rassembler les assets officiels et la dernière maquette approuvée.
- [ ] Développer une Home haute fidélité sans bloc de matières.
- [ ] Tester Desktop XL au viewport CSS 1920 x 1080 ; compléter les tests responsive.
- [ ] Contrôler FR/AR, RTL, clavier, contrastes, performances et contenu authentique.
- [ ] Valider l'interface par le propriétaire avant création d'autres pages.

## P2 — Socle de données et pédagogique (DSI + Data Engineering + Data Scientist + Web)
- [ ] Schéma et dictionnaire de données vérifiés, migrations réversibles.
- [ ] Définir règles transparentes de diagnostic, prérequis et progression avec évaluations sur données synthétiques.
- [ ] Implémenter plugin indépendant mnin-nbda-core.
- [ ] Valider comptes Parent/Élève et cloisonnement des foyers en tests.
- [ ] Introduire le reporting analytique uniquement avec KPI définis et accès contrôlés (Data Analyst).
- [ ] Conserver l'IA pédagogique facultative et non essentielle (AI Engineering).

## P3 — Tests et livraisons (tous selon besoin, DevOps référent)
- [ ] Développer pages supplémentaires seulement après validation design system.
- [ ] Tester sécurité, performance, accessibilité et langues sans chiffres inventés.
- [ ] Construire les ZIP thème et core et les installer sur WordPress propre.
- [ ] Produire rapports de tests factuels, changelog et plan de rollback.
- [ ] Déployer uniquement après autorisation explicite.

## Mesure et responsabilités
Chaque tâche doit préciser un rôle responsable, des preuves et un statut parmi PASS / FAIL / NON TESTÉ / BLOQUÉ. Conserver docs/STATUS.md factuel et daté. Aucune automatisation IA continue n'est garantie par GitHub Actions.
