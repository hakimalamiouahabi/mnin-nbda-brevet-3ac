# MNIN Bridge Pro — AgentGrid v0.8

**Validation technique : 122 tests Python PASS dans GitHub Actions, 700 profils originaux vérifiés et 700 contrats de rôles générés. Zéro nouvel agent ajouté ; zéro session LLM autonome lancée.**

- Code : `agentgrid.py`, `role_briefs.py`, `agentgrid_proof.py`, `agentgrid/profiles-700.json`.
- Outils MCP de lecture : statut, recherche, plan de mission, portefeuille et contrat de rôle.
- Exécution démontrée sans API IA payante : **vérifications déterministes sur des runners hébergés par GitHub**.
- Preuves : https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/actions/runs/38327072681
- Compte rendu et limites : `docs/AGENTGRID_700_NO_NEW_INFRA_NO_PAID_AI_API.md`.
- **Blocage inchangé** : serveur MCP Pro distant non déployé, outils privés non connectés ; aucun passage magique à 700 intelligences autonomes.
- Restrictions Pro officielles : https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt
- Sans serveur personnel oui, sans calcul/infra au sens littéral non : GitHub Actions utilise les machines de GitHub.
- Les connecteurs actuels GitHub/Cloudflare/WordPress restent accessibles **selon leurs propres autorisations**, sans modifier le WordPress MNIN ni supprimer de données D1.

---


# MNIN Bridge v0.5 — Hub de bibliothèques GitHub publiques

**Statut : 11 référentiels GitHub publics et non archivés vérifiés, 6 bibliothèques npm déclarées pour environnement isolé, outils MCP de catalogue enregistrés, serveur ChatGPT non connecté.**

## Registre officiel
`integrations/open_source_registry.json` recense les URL, licences SPDX, compétences et états de connexion de :
Playwright, Lighthouse, axe-core, Pixelmatch, Sharp, SVGO, Three.js, glTF-Transform, WP-CLI, MCP Python SDK et glTF-Validator.

**Distinctions :**
- `catalogued` : GitHub public recensé, pas installé ni exécutable.
- `proposed_runtime_dependency` : dépendance déclarée dans `runner/package.json`, installation uniquement durant des tests/runner autorisés.
- `already_integrated_code` : code source de l'adaptateur présent, ne signifie pas que le navigateur a été lancé.
- `existing_python_dependency` : référence à la dépendance `mcp` de `requirements.txt`, serveur non connecté.

## Les connexions réellement préparées
- BrowserLab : Playwright, 21 formats et captures viewport / pleine page.
- AccessibilityLab : axe-core branché au test navigateur via `MNIN_A11Y_MODE=on` ; contrôles automatiques partiels, pas certificat WCAG.
- VisualDiffLab : `compare-captures.mjs` utilise Pixelmatch et PNGJS ; mêmes dimensions obligatoires, sortie dérivée, jamais de retouche du PNG original.
- AssetLab : Sharp déclaré dans un runner isolé ; module Python interne pour lire dimensions natives PNG/JPEG/WebP, SVG et métadonnées GLB.
- VectorLab : SVGO déclaré et vérifié par smoke test npm ; jamais de réécriture automatique du SVG approuvé.
- GitHub Registry : deux outils MCP de lecture (`bridge_open_source_catalog`, `bridge_open_source_readiness`).

## Sources cataloguées pour intégration ultérieure
Lighthouse, Three.js, glTF-Transform, glTF-Validator, WP-CLI : **aucune intégration opérationnelle déclarée ici**. Leur présence dans le registre ne donne aucun droit ou accès WordPress.

## Installer les dépendances pour test (dans runner isolé)
```bash
cd mnin-bridge/runner
npm install --no-audit --no-fund --no-package-lock
npm run oss:smoke
```
Le pipeline CI `mnin-bridge-oss-checks.yml` valide les packages et les tests Python en parallèle, sans modifier WordPress.
Le workflow QA BrowserLab peut uniquement être demandé avec le site HTML existant dans `site/`, `home/` ou `preview/`. La QA réelle est **BLOQUÉE** sans fichier HTML et runner effectivement exécuté.

## Ce que GitHub et ChatGPT Pro ne font pas automatiquement
Un dépôt public n'est ni une application installée ni un agent. Une connexion GitHub peut lire le code mais ne charge pas ses exécutables dans ChatGPT. Pour appeler les outils dans les conversations ChatGPT Pro classiques, il faut déployer **un serveur MCP HTTPS réellement authentifié**, ajouter le plugin à ChatGPT depuis l'interface et satisfaire les permissions. Le contrôle strict de l'abonnement Pro seul et l'exclusion Work/Codex nécessitent une preuve d'identité de surface qui n'est pas garantie par un dépôt GitHub ou un manifeste.

Sans preuve fiable d'appartenance au plan Pro et à la bonne surface, les outils privés restent bloqués (fail closed). Les bibliothèques open source peuvent avoir un coût d'infrastructure ou d'exécution et leurs licences doivent être respectées.

## Protection de la maquette originale
Pas de régénération non autorisée, pas de redimensionnement présentant le raster d'origine comme une vraie source 8K, pas de publication du PNG original dans un dépôt public. Les captures pleine page doivent garder leur hauteur naturelle et leurs noms documenter largeur, hauteur et viewport.

---

# MNIN Bridge Pro — v0.3 (ChatGPT Pro, conversation classique)

**ÉTAT : code préparé sur branche isolée ; plugin non installé, non déployé et sans serveur d'authentification. 43 tests unitaires PASS sur GitHub Actions (run 38322321083) ; tests OAuth de bout en bout et intégration MCP NON TESTÉS.**

### Autorisation permanente demandée par le propriétaire

La préférence de délégation durable est dans `owner_delegation_policy.json`. Elle couvre les opérations courantes **seulement après** authentification indépendante, confirmation du propriétaire et application des limites. Le fichier de politique constitue une **configuration de permissions projetée**, pas une autorisation OAuth ni une permission de contourner l'hôte ChatGPT.

Le nouveau module `access_policy.py` impose : propriétaire vérifié, audience et émetteur OAuth, client autorisé, preuve indépendante de l'interface ChatGPT standard et preuve vérifiée d'abonnement Pro. Si la preuve Pro/surface n'est pas exposée au serveur par une source digne de confiance, la décision reste **DENY**, et aucune prétention de filtrage « Pro uniquement » n'est permise.

### ChatGPT Pro uniquement, hors Work et Codex

- Cible : conversations normales ChatGPT Pro, usage personnel de l'unique propriétaire autorisé.
- Work et Codex ne sont **ni requis ni considérés comme moteur d'exécution**.
- Le plugin n'autorise pas les appels identifiés de manière fiable comme Work/Codex. Sans identité client/source cryptographiquement fiable, il refuse les outils privés.
- Les plugins OpenAI sont généralement disponibles sur plusieurs surfaces : **le packaging seul ne peut pas prouver ni imposer l'exclusivité Pro ou l'exclusion absolue de Work/Codex**. Une attestation fiable de plan/interface ou une limitation de disponibilité par la plateforme reste nécessaire.
- L'accès externe exige un MCP distant HTTPS et OAuth 2.1, non encore installés.

### Contrôles bloquants V0.3

Tous les outils MCP privés ont une garde `_require_verified_pro_standard_chat()` qui **refuse l'accès à ce stade**, car le validateur OAuth du serveur n'existe pas encore. Ce garde ne peut pas être supprimé par une variable d'environnement ou un booléen fourni par le modèle.

Le droit permanent de créer des missions et d'exécuter des tests isolés après connexion sécurisée n'inclut **pas** la suppression, le déploiement public, l'achat de services, les fusions sur `main`, les changements DNS, les exports de données sensibles ou les modifications WordPress sans autorisation spécifique.

### Outils disponibles dans le code

- `bridge_delegation_policy()` : description non sensible de la délégation (lecture seule).
- `access_policy.evaluate_delegation(...)` : moteur de décision pur côté serveur ; son paramètre `VerifiedPrincipal` ne doit jamais être un paramètre d'outil MCP.
- `skills/chatgpt-pro-operator/SKILL.md` : procédure d'utilisation par ChatGPT Pro standard.
- `tests/test_access_policy.py` : scénarios de blocage Pro non vérifié, Work, Codex, client non reconnu, dépenses, WordPress et opérations destructrices (tests écrits, pas encore exécutés).

### Reste à effectuer

1. Vérifier le niveau d'accès réellement disponible de ChatGPT et la présence d'une attestation fiable de plan/surface ; faute de preuve, ne pas annoncer « Pro uniquement » comme garanti.
2. Implémenter OAuth 2.1, identité serveur et révocation de délégation ; obtenir les identifiants client/audience via l'autorisation effective (ne pas les inventer).
3. Configurer stockage privé et runner isolé dans une infrastructure autorisée, à coût additionnel nul vérifié.
4. Exécuter les tests, audit sécurité, puis installer le plugin depuis ChatGPT standard.
5. Faire un test réel : original Home → SHA256 → capturer 21 écrans → rapport QA ; aucune publication WordPress.

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