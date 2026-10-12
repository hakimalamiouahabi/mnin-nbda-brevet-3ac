# Modèle d'orchestration — 43 profils / 6 équipes / sans API IA payante

## Architecture
**1 Directeur SI, 3 Senior Managers, 3 Managers, 6 Team Leaders, 30 agents spécialisés** ; document normatif : `agents/manifest.json` ; vue arborescente : `agents/org-structure.json`.

| Senior Manager | Manager | Team Leaders (5 experts chacun) |
|---|---|---|
| SM_PRODUCT | M_PRODUCT | TL_PRODUCT_EDTECH + TL_DESIGN_CONTENT |
| SM_ENGINEERING | M_ENGINEERING | TL_WEB_PLATFORM + TL_DATA_AI |
| SM_TRUST | M_DELIVERY | TL_QA_SECURITY + TL_DEVOPS_RELEASE |

## Gouvernance
Le **DSI** arbitre les dépendances, les coûts, l'architecture et les risques. Les **Senior Managers** contrôlent les objectifs et les arbitrages transversaux. Les **Managers** traduisent les objectifs en lots. Les **Team Leaders** distribuent des tâches à leurs 5 spécialistes, contrôlent et consolident les livrables. Les **agents experts** exécutent les missions autorisées et documentent les preuves. Les spécialistes n'ont pas à tous travailler simultanément.

## Exécution réelle
Les fichiers Markdown ne créent pas un runtime d'agents. Dans ChatGPT Work ou Codex, utiliser `docs/WORK_MASTER_START.md` pour mobiliser les rôles disponibles. Si des processus/sous-agents parallèles ne sont pas réellement exposés, exécuter la chaîne **séquentiellement** et notifier le contexte. Aucun agent ni planification 24 h/24 n'est activé du seul fait de ce dépôt. Ne jamais introduire une API IA payante pour donner une illusion d'autonomie.

## Cycle DSI
1. Lire les masters et les décisions vérifiées. Identifier une tâche prioritaire et ses risques.
2. DSI → Senior Manager : problème, sources, contraintes, critères de réussite.
3. Senior Manager → Manager : découpage en lots, points d'intégration, budget nul d'API payante.
4. Manager → Team Leader : backlog local et affectation d'une ou plusieurs tâches à leurs experts.
5. Expert : produire le livrable et sa preuve ; aucun changement sensible non autorisé.
6. Team Leader : revue, regroupement, statut PASS/FAIL/NON TESTÉ/BLOQUÉ.
7. Manager → Senior Manager : synthèse des lots et risques ; expertise QA/Security obligatoire avant livraison sensible.
8. Senior Manager → DSI : preuves et décisions à arbitrer ; DSI clôt ou remet en planification.

## Transfert standard
ID de tâche ; responsable de niveau ; spécialiste assigné ; sources et versions ; état initial ; résultat demandé ; modifications ; commandes/tests réellement exécutés ; preuves avec commits/captures ; risques ; blocages ; besoin d'autorisation ; prochaine action.

## Portes de validation
**G0 Audit** : site WordPress existant analysé en lecture seule, sauvegarde et rollback déterminés.
**G1 Maquette** : Home conforme à l'original approuvé ; si visuel absent, déclarer comparaison impossible.
**G2 Données** : sécurisation Parent/Élève, minimisation et tests autorisés sur jeux fictifs.
**G3 Métier** : scénarios pédagogiques diagnostique/exercice/progrès réellement testés.
**G4 Livraison** : thème et core séparés, ZIP installés sur WordPress propre, QA documentée.
**G5 Publication** : accord humain explicite pour la version ciblée.

## Contrôles essentiels
Aucune API IA payante, aucun stockage externe obligatoire, aucun secret en dépôt, aucune donnée réelle de mineur transmise aux agents, aucun déploiement ni facturation sans autorisation. Statuts limités à PASS / FAIL / NON TESTÉ / BLOQUÉ. GitHub Actions est une CI déterministe, et son quota doit être respecté.
