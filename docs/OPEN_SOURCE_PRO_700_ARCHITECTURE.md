# Organisation existante des 700 profils — ChatGPT Pro et open source

**Statut : architecture proposée, non déployée.** Aucun profil ajouté ou supprimé.
Registre canonique : `agents/manifest-700-target.json` (branche `proposal/organization-700`).
Répartition intangible : 5 DSI, 30 Senior Managers, 60 Managers, 60 Team Leaders, 545 experts = 700 profils et 30 pôles. Le registre de 43 profils `agents/manifest.json` reste inchangé.

## Liaisons open source officielles (références, pas installations)

| Outil | Dépôt officiel | Mission et limitation |
| --- | --- | --- |
| GitHub MCP Server | https://github.com/github/github-mcp-server | Contrôle des dépôts, branches et PR ; n'étend pas les droits MCP personnalisés de ChatGPT Pro |
| Cloudflare API MCP Server | https://github.com/cloudflare/mcp | Inspecter Workers, D1, KV, R2 ; OAuth et permissions nécessaires |
| WordPress MCP Adapter | https://github.com/WordPress/mcp-adapter | Exposer WordPress Abilities ; n'étend pas l'écriture MCP personnalisée de ChatGPT Pro |
| WP-CLI | https://github.com/wp-cli/wp-cli | Diagnostic et maintenance, uniquement après sauvegarde et validation des écritures |
| LangGraph | https://github.com/langchain-ai/langgraph | Gestion d'états et enchaînement des rôles ; ne fournit **aucun modèle** ou infrastructure IA gratuite |
| GitHub Actions | https://docs.github.com/en/actions | Calcul temporaire pour des contrôles déterministes ; pas 700 IA autonomes |

**Ces dépôts ne sont pas installés automatiquement dans ChatGPT Pro.** Les applications GitHub, Cloudflare et WordPress préexistantes servent uniquement dans leurs limites d'accès effectives. ChatGPT Pro assure, en session, le raisonnement attribué aux rôles existants. Des jobs CI peuvent effectuer des tests sans API IA payante, mais ne simulent pas des intelligences supplémentaires.

## Plan d'épuration en trois environnements : audit préalable obligatoire

### Cloudflare D1

- Inventaire des 4 bases existantes, distinction de production et staging, tables, index, tailles, migrations et dépendances Worker.
- Chercher requêtes peu sélectives par `EXPLAIN QUERY PLAN`; ne jamais utiliser `DELETE`, `DROP`, `VACUUM` ni modifier les index en production sans décision.
- Avant chaque maintenance : export vérifié, sauvegarde privée protégée, test de restauration sur copie, protocole de retour arrière.
- Respect des plafonds du forfait Free et des limites quotidiennes D1.

### GitHub

- Inventaire des dépôts, workflows, branches orphelines, artefacts, dépendances et alertes de secrets **sans divulguer les secrets**.
- Ne pas supprimer de dépôt, de branche, d'historique Git ou d'artefact sans contrôle des références et autorisation expresse.
- Activer uniquement les contrôles nécessaires et limiter les permissions des workflows ; dépôts publics : ne déposer ni secrets, ni données personnelles d'élèves.

### WordPress

- Lecture seule : versions et état des plugins, thèmes, options autoload, transients expirés, révisions, métadonnées, médias supposés orphelins.
- Sauvegarde complète **base et fichiers** avec restauration testée sur staging ; mesure avant/après avec critères explicites.
- `wp transient delete --expired`, `wp db optimize` et toute purge restent **désactivés** tant que la validation n'est pas donnée ; ne pas employer de SQL direct sur métadonnées sérialisées.
- Aucun plugin installé ni déployé par ce dossier documentaire.

## Sécurité et exécution

- Commandes et scripts en lecture seule par défaut, zéro clé secrète dans le dépôt.
- Workflow GitHub Actions : `permissions: contents: read`, délai maximum 5 minutes, lancement manuel ou contrôle de PR, aucun accès à Cloudflare/WordPress.
- Chaque validation fournit un résultat PASS/FAIL. Les 700 profils restent en état `TARGET_NOT_DEPLOYED`; la réussite du validateur n'atteste d'aucun agent autonome.
- Aucune tâche à intervalle régulier n'est activée et aucune dépense n'est ajoutée.
