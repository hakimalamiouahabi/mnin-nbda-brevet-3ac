# MNIN Bridge v0.8 — AgentGrid : 700 profils existants, aucun agent ajouté

**Statut : code d'intégration et planification ; ce fichier n'affirme PAS que 700 intelligences artificielles sont en exécution.**

## Résolution des deux blocages dans ChatGPT Pro

### 1) Restrictions d'écriture du MCP personnalisé

Selon l'aide officielle d'OpenAI vérifiée au 13 octobre 2026, ChatGPT Pro peut connecter des MCP personnalisés pour les opérations de lecture et récupération en mode développeur. Le MCP personnalisé à capacités complètes d'écriture/modification reste réservé aux plans Business et Enterprise/Edu :
https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt

**Nous ne contournons pas cette restriction.** Nous utilisons dans la conversation ChatGPT les connecteurs GitHub, Cloudflare et WordPress **déjà autorisés**, dont les permissions sont gérées indépendamment. GitHub Actions exécute ensuite les scripts autorisés et en retourne preuves/logs/artefacts, sans écrire par l'intermédiaire d'un MCP personnalisé interdit. Aucun mécanisme caché d'élévation de privilèges n'est permis.

### 2) « Sans infrastructure ni API », pour 700 profils IA

- **Sans serveur dédié et sans nouvelle API IA payante : possible** pour le *catalogue, la coordination, les vérifications déterministes et les rapports*. GitHub fournit les runners de GitHub Actions et les connecteurs appellent leurs services sous leurs propres permissions.
- **Sans infrastructure au sens strict : impossible** pour exécuter du code ou faire de l'inférence. Les runners GitHub Actions sont bel et bien de l'infrastructure hébergée par un tiers, même lorsque leur utilisation est gratuite sur un dépôt public.
- **Sans aucun appel API : incompatible** avec l'accès automatisé aux services GitHub, Cloudflare et WordPress. Ne pas confondre « sans API IA payante » avec « sans API ».
- **700 LLM autonomes experts simultanés, permanents, sans modèle ni puissance de calcul : impossible.** Les 700 fiches de postes ne sont pas un modèle de langage, un processus indépendant ni une attestation professionnelle.

La solution minimale utilise ChatGPT comme moteur de raisonnement au fil de la conversation, avec les rôles *existants* sélectionnés séquentiellement selon la mission, et GitHub Actions comme moteur de vérification déterministe non-IA. Les limites de fréquence de ChatGPT, de GitHub Actions et des connecteurs restent applicables.

## Intégration des 700 profils EXISTANTS, exactement

Source inchangée : `agents/manifest-700-target.json` sur `proposal/organization-700`.

Copie pour le plugin : `mnin-bridge/agentgrid/profiles-700.json`.

| Niveau | Nombre |
|---|---:|
| DSI | 5 |
| Senior Managers | 30 |
| Managers | 60 |
| Team Leaders | 60 |
| Experts | 545 |
| **Total** | **700** |

La validation porte sur les identifiants uniques, les rattachements parents et la chaîne jusqu'à un des cinq DSI. Le manifest historique des 43 rôles sur `main` est conservé, aucun des 700 profils n'est renommé ou remplacé.

## Fonctions codées dans AgentGrid

- `bridge_agentgrid_700_status` : total, fonctions et cinq directions.
- `bridge_agentgrid_search_roles` : rechercher par nom ou domaine.
- `bridge_agentgrid_plan_mission` : affecter 1 à 15 experts existants et leurs responsables, selon des critères déterministes.
- `bridge_agentgrid_plan_portfolio` : organiser jusqu'à 5 missions avec concurrence prévue de 1 à 3 jobs.
- `bridge_agentgrid_role_brief` : générer une fiche de travail spécifique à l'ID d'un des 700 postes **existants**, à destination du raisonnement humain ou ChatGPT lors d'un échange autorisé.
- `agentgrid_proof.py` : contrôler les 700 ID/hiérarchies dans un job GitHub Actions et publier un rapport JSON horodaté.
- `role_briefs.py` : générer les 700 contrats de rôle utilisables séquentiellement, **pas 700 sessions LLM**.
- Tests GitHub Actions : `.github/workflows/mnin-bridge-agentgrid-700.yml` ; droits `contents: read` uniquement.

Ces outils sont présents dans le code MCP, mais **ne sont pas connectés comme serveur MCP distant dans ChatGPT Pro**. Leur contenu est exploitable depuis GitHub en utilisant le connecteur GitHub déjà installé.

## Missions proposées à la cellule adaptée

1. Home V1.0 : assets, SVG/8K natif, QA visuelle, Playwright sur 21 dimensions, performance.
2. Cloudflare : diagnostic en lecture seule de `mnin-nbda-staging`, excluant les trois autres bases de l'utilisateur.
3. WordPress : audit de staging, sauvegardes, modules et données transitoires sans modification ni purge.
4. GitHub : volumes, artefacts, branches et historique ; aucune suppression automatique.
5. Référentiels pédagogiques marocains : contrôle de cohérence 1AC/2AC/3AC avec les sources officielles vérifiées.
6. Architecture MCP : revue de sécurité et faisabilité Pro sans droits supplémentaires.

**Routage :** 9 experts par mission par défaut, au maximum 15, répartis parmi les directions utiles. Les 700 fiches sont conservées comme *réservoir de compétences*, pas comme 700 instances parallèles. Les équipes peuvent être adaptées selon les résultats QA.

## Matrice de vérité opérationnelle

| Capacité | Statut |
|---|---|
| Copie fidèle du catalogue existant des 700 rôles | Intégrée dans le plugin sur branche |
| Vérification de tous les profils dans GitHub Actions | À confirmer par lien de run PASS |
| Génération de 700 fiches de mission | À confirmer par le run PASS |
| Affectation déterministe de profils aux missions | Codée, tests requis |
| Bibliothèques open source GitHub | 20 projets catalogués sur les versions précédentes, plusieurs testés |
| Navigateur Chromium sur 21 viewports | PASS antérieur sur fixture, pas encore Home réelle |
| Nettoyage Cloudflare / WordPress / GitHub | Aucun ; dry-run uniquement |
| Serveur MCP Pro distant sécurisé | Non connecté, protections OAuth non déployées |
| 700 instances IA indépendantes actives | 0 |
| API IA payante, nouvelle infrastructure dédiée | Aucune mise en service |

## Gouvernance

**Exécution humaine et IA :** le propriétaire valide toujours les opérations présentant un risque : publication WordPress, suppression, frais, changement DNS, fusion sur `main`, secrets et données d'élèves. La préférence d'autorisation durable ne contourne jamais une règle de sécurité, les confirmations des connecteurs ou les permissions OpenAI.

**GitHub Actions :** limiter les permissions du `GITHUB_TOKEN` à `contents: read`, pas de secrets ni de contenus utilisateurs dans les PR publiques ; les scripts de test ne doivent lire que les fixtures ou le catalogue public approuvé.

**Fidélité graphique :** la Home V1.0 reste figée ; un PNG agrandi à 8K n'est pas un asset natif haute résolution et ne doit pas être présenté comme tel.

## Prochaine étape de valeur

Après CI PASS : engager une mission ciblée sur la vraie Home avec les sources approuvées disponibles dans un espace privé, puis documenter les écarts d'assets et de responsive ; en parallèle préparer le bilan d'épuration sans suppression de la base D1 staging. Le déclenchement de tâches à répétition ou d'actions sensibles nécessitera une capacité réellement connectée et autorisée.
