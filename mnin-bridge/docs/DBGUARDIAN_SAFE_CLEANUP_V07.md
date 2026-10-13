# MNIN Bridge DBGuardian v0.7 — entretien Cloudflare, GitHub, WordPress

**Statut : code sur branche d'essai, tests à vérifier en CI, aucune purge.**

## Vérité produit ChatGPT Pro

La documentation OpenAI au 13/10/2026 indique : les MCP personnalisés Pro disposent de droits de lecture/récupération ; les actions personnalisées MCP en écriture complètes restent Business, Enterprise et Edu. Aucun open source ou serveur ne contourne cette permission côté ChatGPT.

Nous utilisons **les connecteurs existants réellement disponibles dans ce chat** (GitHub, Cloudflare et WordPress.com) quand leurs actions sont autorisées ; sinon, des GitHub Actions de CI, exécutées dans GitHub avec les permissions GitHub, peuvent produire des rapports et des artefacts. L'utilisateur confirme séparément les changements destructeurs.

## Étape P0 : lecture seule des trois environnements

**Cloudflare D1** : schéma `sqlite_master`, index, colonnes TTL, métriques et limites, état de Time Travel, export vers dossier privé, estimation des risques et dépendances avant toute commande de suppression. Les autres projets D1 ne sont pas automatiquement dans le périmètre MNIN.

**WordPress** : vérifier le backup Jetpack et la possibilité de restauration ; inventorier transients expirés, révisions, médias et options lourdes en lecture seule, sans désinstaller de plugin ni nettoyer au hasard. La commande officielle `wp transient delete --expired` existe, mais elle reste bloquée sans sauvegarde vérifiée et validation du lot.

**GitHub** : inventorier les branches, commits et objets volumineux (`git-sizer`), artefacts CI, tags/releases et risques de secrets (`Gitleaks`). Un dépôt Git n'est pas une base SQL ; ne jamais forcer l'historique, supprimer des branches non fusionnées ni utiliser `git-filter-repo` sans copie indépendante, inventaire des dépendances et approbation expresse.

## 9 projets open source supplémentaires

Registre : `integrations/open_source_maintenance_registry.json`. Il répertorie Cloudflare Wrangler (`cloudflare/workers-sdk`), `simonw/sqlite-utils`, `simonw/datasette`, `github/git-sizer`, `newren/git-filter-repo`, `gitleaks/gitleaks`, `cli/cli`, `wp-cli/db-command` et `OpenRefine/OpenRefine`.

**État réel** : les dépôts ont été vérifiés publics/non archivés via GitHub. Aucun outil n'est automatiquement installé par son inscription au registre. L'intégration sqlite-utils est testée en CI sur une base synthétique, pas sur une vraie base Cloudflare.

## Fonctions codées

- `audit_sqlite_snapshot(filename)`: uniquement une copie SQLite locale autorisée ; pas de colonnes de données ni de valeurs personnelles retournées, `query_only`, URI `mode=ro`.
- `preview_cleanup(context, candidates)`: simulation, risque, preuve sauvegarde manquante, interdiction d'exécuter quoi que ce soit même si le client prétend `backup_verified=true`.
- `wordpress_readonly_plan()`: liste les contrôles sans écrire et commandes sensibles à examiner.
- `github_readonly_plan(repository)`: inventaire des risques, sans suppression d'historique.
- `cloudflare_readonly_plan(database)`: contrôle structurel D1 sans SQL direct.
- MCP : `bridge_sqlite_snapshot_audit` (protégé par OAuth Pro non implémenté), `bridge_cleanup_dry_run`, `bridge_wordpress_cleanup_plan`, `bridge_github_cleanup_plan`, `bridge_cloudflare_cleanup_plan`. **Pas de véritable connexion de ce serveur à ChatGPT.**

## Règles de sûreté

- Aucun `DELETE`, `TRUNCATE`, `DROP`, `VACUUM`, `git push --force`, suppression de plugins, médias ou branches.
- Pas de modification de WordPress ou d'accès aux données réelles d'élèves.
- Le dépôt peut être public : **ne jamais exporter de schémas sensibles, secrets, sauvegardes ou données personnelles** vers le dépôt.
- Sauvegarder hors du système concerné et faire un test de restauration lorsque cela devient nécessaire.
- Le mode Pro n'autorise pas une expansion magique des permissions MCP. OAuth réel, quotas, consentement ponctuel sur tâches sensibles et limitations du fournisseur restent applicables.
- Tout lot doit avoir un rapport avant/après, un identifiant de backup et des critères de réversibilité.

## P1 à P3

P1 : CI PASS sur fixture ; confirmer les données structurales sans contenu personnel.

P2 : rapport détaillé read-only de la base D1 MNIN et de l'installation WordPress ; établir les tables candidates, les tailles, les relations, les TTL réels et les risques. Aucune suppression.

P3 : proposer à l'utilisateur une liste précise et justifiée d'opérations ; exécuter uniquement les opérations approuvées, compatibles avec les capacités réelles des connecteurs. Aucun contournement des limitations MCP Pro.

Références : https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt ; https://developers.cloudflare.com/d1/reference/time-travel/ ; https://developer.wordpress.org/cli/commands/transient/delete/ .
