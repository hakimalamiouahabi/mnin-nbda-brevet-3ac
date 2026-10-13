# MNIN Bridge Pro v0.8 — six outils open source réellement exécutés

**Statut :** chaîne GitHub Actions vérifiée sur **fixtures publiques fictives**, mais aucun MCP personnalisé déployé ni connecté à ChatGPT Pro, et aucun WordPress modifié. Travail exclusivement dans le chat standard, hors Work et Codex.

**Preuves :** [rapport de développement v0.8](docs/OPEN_SOURCE_EXECUTION_V08.md) et [exécution GitHub Actions #4](https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/actions/runs/38325215110). Six outils ont réellement fonctionné sur les fixtures : HTML-Validate, Prettier, SVGO, Sharp, Playwright et axe-core. Les cinq viewports du mode rapide ont été exécutés dans le navigateur ; les deux jobs sont PASS. **Il ne s'agit PAS d'un audit du site réel.**

[Catalogue des huit projets](docs/OPEN_SOURCE_INTEGRATIONS_V07.md) : Lighthouse et WordPress Coding Standards sont simplement référencés, pas encore exécutés.

**Depuis ChatGPT Pro :** l'application GitHub déjà autorisée permet les écritures permises (branches, fichiers, PR) ; GitHub Actions exécute le code libre sur des commits. Ceci ne contourne pas les limites de modification MCP personnalisée. L'autorisation propriétaire permanente est enregistrée comme préférence dans `owner_delegation_policy.json`, dans le respect des permissions et confirmations du fournisseur.

**Conditions inchangées :** aucune API IA payante, aucun budget ajouté, aucun déploiement WordPress, aucun agent autonome en fonctionnement, aucun secret ni donnée de mineur dans le dépôt public. La preuve d'abonnement Pro côté serveur n'est pas implémentée.

---

# MNIN Bridge — plateforme MCP privée (prototype v0.2)

**STATUT VÉRIFIÉ : code publié sur une branche d'essai, NON DÉPLOYÉ, NON CONNECTÉ, aucun worker ni sous-agent réellement lancé.**

Le manifeste portable est dans `plugin.json` ; les instructions spécialisées sont dans `skills/`.
Un paquet de fichiers ne donne **pas** de permissions nouvelles à ChatGPT : seules une connexion MCP authentifiée et des ressources d'exécution réelles le permettront.

## Ajouts V0.2

- Contrôle des missions dans `mission_control.py` : cinq types autorisés, paramètres validés, registre persistant SQLite, idempotence, plan d'intervention et événements auditables.
- Sept nouveaux outils MCP (catalogue, validation, proposition, consultation, liste, aperçu, journal). Une proposition **ne déclenche aucune exécution**.
- Tests supplémentaires dans `tests/test_mission_control.py` : présents dans GitHub, **non exécutés**.
- BrowserLab : matrice « smoke » de 5 écrans ou matrice complète de **21 écrans**, captures viewport/pleine page, erreurs navigateur, images cassées et alertes de densité des images raster.
- `docs/ARCHITECTURE_ENTERPRISE_V02.md` : architecture d'exécution par étapes, permissions, OAuth, workers isolés et intégration WordPress future.
- Déclenchement de workflow en V0.2 : **refusé côté serveur même si le modèle envoie une approbation booléenne**. Une autorisation indépendante et authentifiée reste à développer.

## Conséquences

- Le serveur local n'a pas d'OAuth : **ne jamais l'exposer publiquement en l'état**.
- La base SQLite locale ne persiste pas sur un hébergement à système de fichiers éphémère. Le choix d'une base durable privée précède tout déploiement.
- Le dépôt GitHub est actuellement déclaré **PUBLIC** : aucune image originale non publique, donnée scolaire nominative ou clé secrète ne doit y être ajoutée.
- L'installation et le lancement des workflows ne sont pas inclus.
- Les 700 profils IA restent un organigramme cible documenté, pas 700 modèles lancés.

## Étape suivante, à approuver séparément

Exécuter les tests, procéder à la revue de sécurité, choisir OAuth 2.1, stockage privé, hébergement et plafonds de coût, puis seulement connecter un endpoint HTTPS authentifié dans ChatGPT.

---

# MNIN Bridge — plugin MCP privé (prototype v0.1)

**STATUT : code créé, PAS connecté à ChatGPT, PAS déployé, PAS installé sur WordPress.**

## Objectif

Donner à ChatGPT/Codex des outils d'exécution sûrs et vérifiables plutôt que supposer un accès à Codex, Work, WordPress, au navigateur ou à des fichiers binaires non montés.

Fonctions codées :
- inventorier les noms d'images originales disponibles dans un dossier privé expressément monté ;
- mesurer le SHA-256 et les dimensions natives d'un PNG **sans toucher aux octets** ;
- préparer un déclenchement GitHub Actions de QA de page HTML locale, **désactivé** tant que l'authentification forte n'est pas prête ;
- consulter le statut réel d'un job QA et ses artifacts, si les identifiants d'accès sont configurés ;
- enregistrer des captures navigateur viewport + pleine page sur cinq tailles de référence via Playwright.

## Éléments livrés

- bridge_core.py : fonctions testables, contrôles de chemins, API GitHub limitée.
- server.py : six outils MCP, sans déploiement internet.
- tests/test_bridge_core.py : tests standard library.
- runner/home-qa.mjs : captures et tests automatiques du HTML local.
- .github/workflows/mnin-bridge-home-qa.yml : workflow manuel QA (présent uniquement sur cette branche).

## Lancer les tests locaux

Depuis la racine du dépôt :

    python3 -m unittest discover -s mnin-bridge/tests -v

## Exécuter le serveur MCP localement

    cd mnin-bridge
    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r requirements.txt
    export MNIN_ASSET_ROOT=/chemin/du/dossier/prive-des-originaux
    export MNIN_ENABLE_DISPATCH=0
    python server.py

**Le serveur ne doit PAS être exposé sur internet tel quel.** Il manque OAuth 2.1, validation des autorisations par utilisateur, protection du service et journalisation des appels. L'installation d'un plugin nécessite un serveur MCP sécurisé sur HTTPS ou un tunnel sécurisé validé. Le propriétaire doit connecter lui-même le plugin depuis ChatGPT Plugins.

## Limites très importantes

1. Une image intégrée dans une conversation ne devient pas automatiquement un fichier disponible sur un serveur externe. Les originaux doivent être transmis vers un stockage privé réellement accessible au service.
2. Le dépôt GitHub est actuellement signalé comme PUBLIC par GitHub : ne pas y importer de documents d'élèves, d'identifiants, ni des images privées non approuvées pour la publication.
3. Le workflow GitHub Actions manuel ne peut être déclenché via workflow_dispatch qu'après validation et présence sur la branche par défaut. Aucun job n'a été déclenché par la livraison du code.
4. Le QA ne fonctionne que si la branche cible contient une page HTML dans site/, home/ ou preview/. Le WordPress existant n'est ni copié, ni modifié, ni testé automatiquement.
5. Les tests de QA sont des contrôles d'absence de débordement horizontal, de chargement des images et d'erreurs JS ; ils ne certifient ni la fidélité pixel à pixel, ni l'accessibilité complète, ni les performances réelles.
6. Aucun agent IA permanent n'est créé. Les 43/700 profils documentés restent des profils, sans processus autonome.
7. L'utilisation d'un runner ou d'un hébergeur peut dépendre de quotas et des politiques de facturation ; aucun nouveau service n'a été activé.

## Étapes restant à autoriser

- revue de sécurité et construction de l'authentification OAuth ;
- validation d'un hébergement/tunnel sécurisé pour serveur MCP ;
- configuration privée des permissions GitHub et du dossier d'assets ;
- validation de l'installation du workflow sur la branche par défaut ;
- connexion volontaire du plugin ChatGPT depuis l'interface ;
- premier test bout en bout documenté, avec un fichier factice et une page HTML fictive ;
- connexion ensuite à la vraie Home, ses assets approuvés et ses 21 viewports.

## Règles immuables

Aucune API IA payante, aucune dépense non autorisée, aucune publication WordPress ni déploiement de production sans validation. La maquette officielle MNIN NBDA V1.0 reste figée. Les originaux ne sont ni redessinés ni redimensionnés par le calcul d'empreinte.

Références :
- https://developers.openai.com/plugins/build/mcp-server
- https://developers.openai.com/plugins/build/auth
- https://developers.openai.com/plugins/quickstart
- https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow