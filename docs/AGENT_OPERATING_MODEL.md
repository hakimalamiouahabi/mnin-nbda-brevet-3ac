# Modèle d'orchestration — 8 rôles IA, sans API IA payante

## Vue d'ensemble
**DSI = coordinateur.** Sept spécialistes fournissent analyses, code, tests et rapports. Les instructions sont adaptées à ChatGPT Work / Codex / GitHub connectés. Un fichier de rôle n'installe ni une instance indépendante, ni un ordonnanceur permanent.

## Règle d'activation
Un cycle démarre uniquement lorsqu'un utilisateur ouvre Work avec docs/WORK_MASTER_START.md, ou lorsqu'un déclencheur Work effectivement autorisé/configuré le permet. L'orchestrateur lit les fichiers du dépôt et **assume les rôles un par un** si Work ne peut pas lancer de véritables agents parallèles.
Aucune utilisation directe d'une API IA payante, clé OpenAI ou wallet. GitHub Actions exécute seulement des tests déterministes ; il ne fournit pas une IA autonome.

## Entrées obligatoires
- AGENTS.md et les prompts masters V4.2 + Home Desktop XL.
- docs/STATUS.md, docs/ROADMAP.md, décisions les plus récentes.
- État du thème WordPress MNIN NBDA V4 audité, **avant** toute écriture.
- Référence visuelle originale quand disponible : sinon aucune affirmation pixel-perfect.

## Workflow d'un cycle
1. **DSI** : audit de l'état, choix d'une tâche P0 ou P1, risques, statut et acceptation.
2. **Design** : spécification UI et contenus si tâche interface ; **Data Engineering** : contrat de données si tâche backend.
3. **Data Scientist** : protocole diagnostic/mesures si tâche pédagogique ; **Data Analyst** : définition KPI si reporting ; **AI Engineering** : architecture facultative/local, seulement après besoin validé.
4. **Web Dev** : implémentation, tests, commit et rapport. Ne pas déployer.
5. **DevOps** : contrôles, ZIP éventuels et vérifications de reproductibilité ; aucun lancement automatique WordPress.
6. **DSI** : revue croisée et mise à jour des statuts factuels ; tâche suivante ou arbitrage nécessaire.

Le DSI peut sauter les spécialistes non pertinents pour une tâche. Ne pas fabriquer du travail Data Science ou IA pour un simple correctif CSS.

## Contrat de transfert (handoff)
Chaque tâche doit comporter :
- ID et titre ; propriétaire du rôle ; description de l'objectif.
- Sources validées ; hypothèses séparées des faits ; exclusions ; dépendances.
- Modifications/fichiers proposés ; critères d'acceptation ; tests.
- Preuves (commit, sorties réelles, captures si disponibles) et statut PASS / FAIL / NON TESTÉ / BLOQUÉ.
- Risques de confidentialité, coût, sécurité et conformité.
- Décision attendue du propriétaire si changement visible/sensible.

## Portes de validation
**Gate 0 — Audit** : état réel du WordPress existant et sauvegarde possible. Sans preuve, pas d'écrasement du site.
**Gate 1 — Maquette Home** : validation du rendu par propriétaire avant propagation des composants.
**Gate 2 — Données mineurs** : minimisation, ségrégation, autorisations, tests d'accès ; pas de donnée réelle dans Git.
**Gate 3 — Fonction pédagogique** : scénarios fonctionnels réels et preuves.
**Gate 4 — Livraison** : ZIP réellement installés et testés sur WordPress propre, QA et rollback.
**Gate 5 — Déploiement** : autorisation explicite de la version ciblée.

## Sécurité des branches et des actions
Développement sur branche de travail lorsque possible ; changements circonscrits ; aucune élévation de privilèges ni partage d'identifiants. Ne jamais installer, activer, supprimer une extension ou modifier le site, l'hébergement, les DNS, les données d'élèves, un coût ou une publication sans validation explicite.

## Critères d'arrêt
Le cycle se termine quand le temps/la session/l'outil se termine, lorsqu'une validation humaine est obligatoire, quand une anomalie bloquante apparaît, ou quand les critères vérifiables sont atteints. Ne pas boucler indéfiniment sur des erreurs sans nouvelle information. Aucune promesse de disponibilité 24 h/24 sans déclencheurs configurés et traces d'exécution.

## Suivi
docs/STATUS.md : état général daté ; docs/BACKLOG.md si créé : tâches ; docs/DECISIONS.md si créé : arbitrages ; GitHub : commits et preuves d'exécution.
