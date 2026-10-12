# MNIN Bridge Pro 0.7 — huit projets GitHub open source

**Situation :** l'intégration au dépôt GitHub n'est PAS une connexion native de ces huit dépôts comme applications dans ChatGPT. Le dépôt GitHub existant reste utilisable directement avec l'application GitHub autorisée ; le serveur MCP custom n'est pas déployé/connecté. Les logiciels et références ont une licence publique, mais leurs dépendances et usages restent à vérifier avant distribution.

## Référentiel vérifié auprès des dépôts officiels

| Projet public non archivé | Licence amont | Rôle pour MNIN NBDA | État réel du code dans cette branche |
|---|---|---|---|
| https://github.com/microsoft/playwright | Apache-2.0 | 21 formats responsive et captures | Déjà intégré au runner manuel |
| https://github.com/dequelabs/axe-core | MPL-2.0 | Règles d'accessibilité en navigateur | **Code raccordé** à Playwright ; tests d'exécution non vérifiés |
| https://github.com/html-validate/html-validate | MIT | Contrôle HTML hors ligne | **Commande raccordée** au workflow manuel ; tests d'exécution non vérifiés |
| https://github.com/GoogleChrome/lighthouse | Apache-2.0 | Mesures instrumentées, performance/SEO | Catalogue + parcours proposé ; non installé |
| https://github.com/svg/svgo | MIT | Optimiser les copies de SVG approuvés | Catalogue + parcours proposé ; non installé |
| https://github.com/lovell/sharp | Apache-2.0 | Inspection et conversions d'images | Catalogue + parcours proposé ; non installé |
| https://github.com/WordPress/WordPress-Coding-Standards | MIT | PHPCS thème et plugin WordPress | Catalogue + parcours proposé ; aucune source PHP approuvée dans le dépôt |
| https://github.com/prettier/prettier | MIT | Cohérence HTML/CSS/JS | Catalogue + parcours proposé ; non installé |

**Aucune acquisition d'API IA payante.** Un projet logiciel libre n'est pas nécessairement une infrastructure d'exécution gratuite, notamment si on héberge un service ou consomme des minutes CI facturables. Le serveur vérifie son coût et son périmètre avant tout déploiement.

## Développements effectifs

- `open_source_hub.py` : huit dépôts publics vérifiés, URLs, licences, types de tâches, état d'intégration et prérequis.
- MCP `bridge_open_source_catalog(domain?)` : inventaire filtrable, **aucun clonage automatique**.
- MCP `bridge_open_source_pipeline(mission)` : flux proposé pour Home, médias, WordPress, accessibilité bilingue. Ne lance aucun binaire à lui seul.
- `site_auditor.py` : contrôle **hors réseau**, sur un répertoire local expressément configuré `MNIN_SITE_ROOT`, SHA-256, dimensions natives PNG/JPEG/WebP, anomalies SEO/HTML/RTL et plan de correction P0 à P2 ; sources SVG inspectées uniquement comme fichiers vectoriels, sans rendu.
- `runner/home-qa.mjs` : Playwright existant + injection de l'axe-core public, capturant les violations WCAG automatisables. Le navigateur refuse les requêtes HTTP externes et WebSocket et bloque les service workers. Ce n'est pas une isolation réseau complète et les fichiers HTML non approuvés ne doivent pas être exécutés.
- `.github/workflows/mnin-bridge-home-qa.yml` : workflow **manuel uniquement**, installe des versions npm explicitement spécifiées de Playwright, axe-core et HTML-Validate sur un runner temporaire. Le workflow refuse les chemins HTML hors `site/`, `home/`, `preview/` et n'accède pas au WordPress live.

### Exemple de mission de diagnostic local

L'administrateur fournit une **copie locale approuvée** sous :
```
MNIN_SITE_ROOT=/emplacement/prive/
MNIN_SITE_ROOT/site/index.html
MNIN_SITE_ROOT/site/images/logo.png
```
Les chemins représentés sont des exemples, pas des fichiers réels.

Pour le contrôle du HTML et des images, l'outil `bridge_audit_local_home("site/index.html", target_dpr=2)` renvoie un rapport et des actions proposées. Il ne corrige pas automatiquement les pages et ne modifie pas WordPress. La valeur `alt=""` est admissible pour une image purement décorative et l'avertissement de résolution se fonde sur la largeur HTML déclarée, pas nécessairement la largeur CSS réelle.

Pour la QA navigateur, le workflow manuel attend une page HTML existante dans la branche et crée des captures + `report.json`, uniquement après un run GitHub effectivement lancé.

## Normes et limites
- **Accessibilité** : axe-core signale une partie seulement des problèmes ; pas de certification WCAG.
- **Performance** : aucun score Lighthouse ni Core Web Vitals sans exécution instrumentée.
- **Assets** : originaux inchangés, pas de faux upscale 8K ; SVG vectoriels à auditer avant mise en ligne.
- **Sécurité** : GitHub est public ; ne pas y déposer originaux non publiables, données d'élèves, secrets ou journaux sensibles.
- **Abonnement** : cible ChatGPT Pro / chat standard ; le serveur personnalisé n'a pas de preuve fiable d'abonnement ou de surface et n'est pas connecté. Work et Codex exclus des missions.
- **Délégation permanente** : accord-cadre du propriétaire documenté, révocable ; aucun privilège au-delà des capacités vérifiées, des droits OAuth, des contrôles des applications et des confirmations obligatoires.

## Vérifications
```sh
python3 -m compileall -q mnin-bridge
python3 -m unittest discover -s mnin-bridge/tests -v
```
Le workflow `validation.yml` exécute ces commandes sur les pull requests, sous réserve que GitHub Actions soit effectivement actif. **Aucun statut PASS sans exécution observée.**

Les tests navigateur supplémentaires exigent un véritable fichier HTML dans la branche. Les commandes de la suite du dépôt ne contactent aucune API IA payante.

## Prochain ordre d'intégration
Lighthouse dans un environnement isolé et explicitement approuvé, ensuite la validation SVG sur copies (SVGO), puis Sharp pour inspection/conversions opt-in, et WordPress Coding Standards dès disponibilité des fichiers PHP. Ne pas ajouter simultanément une chaîne de dépendances inutile.
