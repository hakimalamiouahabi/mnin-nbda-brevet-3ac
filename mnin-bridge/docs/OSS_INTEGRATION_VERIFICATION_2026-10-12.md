# DSI — Résultat des intégrations GitHub open source (12 octobre 2026)

## Périmètre
Branche `feature/mnin-bridge-open-source-v05` — pull request **#12** en brouillon, base `feature/mnin-bridge-pro-delegation-v03`.

**Objectif :** compléter MNIN Bridge pour un usage futur dans ChatGPT Pro standard, sans Work ni Codex. **Aucune installation directe dans ChatGPT** n'est impliquée par une modification GitHub.

## Dépôts publics vérifiés — 11 / 11
- microsoft/playwright (Apache-2.0)
- GoogleChrome/lighthouse (Apache-2.0)
- dequelabs/axe-core (MPL-2.0)
- mapbox/pixelmatch (ISC)
- lovell/sharp (Apache-2.0)
- svg/svgo (MIT)
- mrdoob/three.js (MIT)
- donmccurdy/glTF-Transform (MIT)
- wp-cli/wp-cli (MIT)
- modelcontextprotocol/python-sdk (MIT)
- KhronosGroup/glTF-Validator (Apache-2.0)

Catalogue complet avec liens, notices de licences et états réels :
`integrations/open_source_registry.json`.
Les licences open source ne signifient pas que les ressources cloud, le calcul ou les modèles IA sont gratuits.

## Pipeline de test réel
Run **MNIN Bridge - OSS integration checks** :
https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/actions/runs/38324156130

| Vérification | Statut | Preuve |
|---|---|---|
| Projets publics et non archivés | PASS | Métadonnées vérifiées par connecteur GitHub pour 11 repos |
| Registre Python/URL/licences | PASS | Tests inclus dans les 68 tests Python |
| Ensemble des tests Python | PASS | `Ran 68 tests ... OK` dans le job registry-python |
| Installation des bibliothèques npm | PASS | 35 packages installés dans l'environnement CI isolé |
| Importation / compatibilité de 6 bibliothèques npm | PASS | `npm run oss:smoke` |
| Contrôle syntaxe scripts Node | PASS | `node --check` |
| 21 captures pleine page réellement exécutées | NON TESTÉ | Aucun HTML Home complet approuvé exécuté par le runner |
| Comparaison pixel à pixel de la Home approuvée | NON TESTÉ | Référence et captures n'ont pas la même dimension native |
| Contrôle axe-core de la vraie Home | NON TESTÉ | Injecteur codé, pas encore exécuté sur la vraie Home |
| Plugin connecté à ChatGPT Pro via OAuth | BLOQUÉ | Aucun serveur authentifié configuré |
| Exclusivité Pro et exclusion Work/Codex | NON CERTIFIÉ | Aucune attestation fiable de plan/surface dans MCP jusqu'ici |
| Écriture WordPress | NON EFFECTUÉE | Interdite sans autorisation spécifique |

Le pipeline CI des 43 profils historiques est également passé sur le commit testé, mais **ne constitue pas une activation d'agents**.

## Niveau de connexion véridique
- 11 projets **référencés** dans MNIN Bridge.
- 6 dépendances **déclarées et effectivement testées en CI** : Playwright, axe-core, Pixelmatch, PNGJS, Sharp et SVGO.
- 3 adaptateurs intégrés au code BrowserLab/VisualDiff : Playwright, axe-core, Pixelmatch.
- Les autres projets sont soit dépendance testée sans pipeline complet, soit simplement catalogués.
- L'exécution distante est bloquée par défaut et toute opération sensible nécessite des autorisations indépendantes.

## Sûreté et qualité
- Aucun modèle payant, aucune API IA payante ajoutée.
- Aucun service Render/Cloudflare créé par cette opération.
- Aucune modification WordPress.
- Aucune donnée sensible ni illustration privée dans le dépôt public.
- Conserver les originaux et leurs empreintes, ne jamais présenter l'upscaling comme une résolution native 8K.
- Avant exploitation production : audit de dépendances, génération/verrouillage d'un `package-lock.json` révisé (versions transitives), revues des licences et de leurs notices, contrôle de consommation des ressources, OAuth 2.1 et scopes serveur.

## Prochaine opération déterminante
Connecter un **endpoint MCP HTTPS authentifié** à ChatGPT (action explicite de l'utilisateur), faire confirmer l'identité via un canal fiable, configurer un stockage privé, et exécuter une mission réelle de bout en bout sur la Home V1.0 : original vérifié → captures 21 viewports → analyse accessibilité/densité → rapport QA → validation propriétaire.
