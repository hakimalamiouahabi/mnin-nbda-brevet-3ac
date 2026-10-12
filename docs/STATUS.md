# État vérifié — 12 octobre 2026

## Organisation GitHub désormais enregistrée
- **43 profils définis** dans le dépôt privé `hakimalamiouahabi/mnin-nbda-brevet-3ac` : 1 DSI + 3 Senior Managers + 3 Managers + 6 Team Leaders + 30 spécialistes.
- Arborescence et rattachements dans `agents/manifest.json` et `agents/org-structure.json` ; 6 équipes de 5 agents.
- Tous les profils ont une fiche dédiée : DSI (`agents/01-directeur-si.md`), 12 encadrants (`agents/leadership/`), 30 experts (`agents/02-...` à `agents/31-...`).
- Instructions communes, modèle de transfert, démarrage Work et roadmap mis à jour pour la structure à 43 rôles.
- CI de vérification structurelle adaptée à l'organigramme ; workflow déclenchable manuellement ou via pull request. **Aucun résultat d'exécution de cette nouvelle CI n'a encore été vérifié**.
- Deux prompts masters déjà enregistrés : V4.2 WordPress et Home Desktop XL.

## Existant WordPress vérifié précédemment
- Site WordPress.com staging `intellego718821273.wpcomstaging.com` accessible ; pas encore lancé publiquement.
- Thème actif : MNIN NBDA V4 (slug `mnin-nbda`).
- Extensions actives observées : WordPress Agent, Gutenberg, Jetpack, Page Optimize, Akismet, CoBlocks, Gravatar Enhanced, Layout Grid.
- **Aucune extension WordPress activée/désactivée par cette opération ; aucun déploiement WordPress**.

## Exécution à ne pas confondre avec la configuration
- **0 / 43 instances autonomes indépendantes lancées ou vérifiées.** Le dépôt contient des définitions de rôles, pas un runtime IA permanent.
- Aucune tâche Work récurrente n'a été créée dans cette opération.
- Aucune clé API IA payante, aucun wallet ou service payant ajouté.
- Les limites de plan Work/Codex et les quotas GitHub Actions n'ont pas été certifiés.
- Aucun test d'installation des ZIP thème/core ni essai de fonctionnement sur une WordPress propre n'a été exécuté.

## Backlog immédiat
- [#1](https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/issues/1) DSI : audit **en lecture seule** du thème/site existant.
- [#2](https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/issues/2) Design : contrôler la disponibilité de la maquette Home approuvée et ses écarts.
- [#3](https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/issues/3) DevOps : confirmer l'exécution effective des contrôles GitHub.
- Décision ouverte : V4.2 cible Brevet 3AC, la Home Desktop XL mentionne aussi 1AC et 2AC ; ne pas trancher sans validation.

## Action de démarrage
Dans ChatGPT Work, donner `docs/WORK_MASTER_START.md` comme instruction au DSI avec accès au dépôt privé. Work peut exécuter les rôles selon les outils disponibles ; leur lancement parallèle et programmation automatique restent à activer/vérifier.

## Cycle DSI du 12 octobre 2026 — audit lancé
Rapport : [AUDIT_EXISTANT.md](AUDIT_EXISTANT.md). Snapshot audité : 2648716caeae74c80d76594cd81d47157b08977e.
- Coordination réelle : session DSI principale + deux sous-agents temporaires DevOps/Design ; responsabilités de la chaîne Web traitées séquentiellement. Les 43 profils restent un référentiel, aucune exécution permanente configurée.
- PASS local : python3 scripts/validate_workspace.py, exit 0, 43 profils et six équipes de cinq. Aucun code PHP dans le dépôt.
- CI du commit audité : NON TESTÉ, zéro workflow run retourné. Dernier run historique failure ; cause non vérifiée (logs indisponibles). Aucun workflow lancé.
- WordPress live : MNIN NBDA V4 actif, thème classique ; 11 extensions dont 8 actives et 3 inactives. Aucun changement.
- Une page brouillon Darija ID 86, template page-home-darija.php, contenu vide ; zéro média retourné. Les anciens compteurs user_sites ne valent pas inventaire détaillé.
- Sauvegarde fournisseur : active, 3 sauvegardes, dernière tentative finished et non échouée ; restauration NON TESTÉ.
- Rendu navigateur : « À venir prochainement ». Comparaison Home NON TESTÉ ; sources du thème BLOQUÉ (absentes du dépôt et non obtenues).
- Réponses confidentialité contradictoires entre user_sites et settings.get, à vérifier sans écriture.
- Visuels absents du dépôt ; candidats maquettes/logo retrouvés dans les fichiers personnels par métadonnées, approbation et pixels non contrôlés.
- Conflits périmètre 3AC/1AC–3AC et nomenclature Gates conservés sans arbitrage. Ticket #3 encore rédigé pour huit agents.
- Audit global BLOQUÉ pour clôture ; tickets #1–#3 restent ouverts. Plan P0/P1 et dépendances dans le rapport.
- Zéro modification WordPress, installation, publication, dépense ou API IA payante. Documentation GitHub uniquement actualisée.
