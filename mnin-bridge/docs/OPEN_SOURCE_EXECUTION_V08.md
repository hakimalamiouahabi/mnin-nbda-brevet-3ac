# MNIN Bridge Pro v0.8 — GitHub open source exécuté depuis ChatGPT Pro standard

**Référentiel :** branche `feature/mnin-bridge-oss-execution-v08` du dépôt public MNIN NBDA.

## Ce qui fonctionne réellement (preuve GitHub Actions)

Sur une page `preview/oss-smoke.html` et un SVG `preview/oss-smoke.svg` **entièrement fictifs et publics** :

| Outil officiel (GitHub) | Mode d'intégration | Preuve |
|---|---|---|
| [HTML-Validate](https://github.com/html-validate/html-validate) | npm versionnée, validateur HTML en CI | PASS |
| [Prettier](https://github.com/prettier/prettier) | npm versionnée, mise en forme en mémoire | PASS |
| [SVGO](https://github.com/svg/svgo) | npm versionnée, optimisation d'une copie en mémoire | PASS |
| [Sharp](https://github.com/lovell/sharp) | npm versionnée, inspecte le SVG et génère un aperçu temporaire | PASS |
| [Playwright](https://github.com/microsoft/playwright) | navigateur Chromium sur cinq formats d'écran | PASS du job navigateur |
| [axe-core](https://github.com/dequelabs/axe-core) | règles WCAG automatiques exécutées dans Playwright | PASS du job navigateur |

**Vérification réelle :** workflow `MNIN OSS integration smoke (public fixtures)`, run [#4](https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/actions/runs/38325215110). Ses deux jobs se sont terminés avec la conclusion `success` ; les quatre tests de bibliothèque étaient `PASS` et `failed=0`. La page fictive a été contrôlée en mode `smoke` à cinq viewports.

**Tests complémentaires déjà réalisés :** le workflow `Validation organigramme (sans API)` sur la même branche exécute les tests Python, la validation de l'organigramme et une vérification syntaxique JavaScript.

**Référencés, non exécutés à ce stade :** [Lighthouse](https://github.com/GoogleChrome/lighthouse) (métriques réelles performance/SEO) et [WordPress Coding Standards](https://github.com/WordPress/WordPress-Coding-Standards) (lint PHP sur des sources WordPress approuvées). Ne leur attribuer aucun PASS.

## Pourquoi cette architecture peut écrire depuis ChatGPT Pro

L'application **GitHub déjà connectée** à ChatGPT dispose, si le compte autorise les actions, d'opérations réelles pour créer des branches, écrire des fichiers et ouvrir des pull requests. En retour, GitHub Actions exécute les logiciels open source **sur les commits de cette branche**. Les outils ne deviennent pas huit apps ChatGPT autonomes.

```text
ChatGPT Pro (chat standard)
  └── Application GitHub autorisée
       ├── branche feature/* et commits + PR brouillon
       └── GitHub Actions (repo public, standard ubuntu-latest)
            ├── HTML-Validate + Prettier + SVGO + Sharp
            └── Playwright/Chromium + axe-core
                 └── rapports + captures sur fixture publique
```

Cela **n'augmente pas** les droits des serveurs MCP personnalisés sur ChatGPT Pro. Une écriture sur WordPress doit passer par une application réellement autorisée à agir sur le site (par exemple WordPress.com lorsque connectée), avec les validations propres à celle-ci ; ce workflow ne réalise aucune écriture WordPress.

## Sécurité, droits et gratuité

- Workflow : `contents: read`, runner `ubuntu-latest`, timeout borné, paquets npm versionnés, aucune clé API IA.
- `preview/oss-smoke.html` n'est ni le site réel ni une maquette approuvée. Aucun original privé, identifiant, donnée d'élève, secret ou media sous copyright non autorisé n'est téléchargé vers GitHub.
- Les règles axe-core ne certifient pas entièrement les WCAG. Les scores Core Web Vitals/Lighthouse et fidélité pixel au design officiel restent **NON TESTÉS**.
- Les runners standards GitHub Actions pour les dépôts publics sont fournis gratuitement selon la documentation GitHub ; le stockage des artefacts et les runners spéciaux ont des règles distinctes.
- Aucun usage Work ou Codex. Aucune API IA payante. Aucune fusion sur `main` ni publication WordPress automatique.
- `owner_delegation_policy.json` conserve la préférence du propriétaire de délégation permanente maximale **dans les permissions effectives** et les contrôles obligatoires. Elle ne donne pas de permissions OAuth supplémentaires.

## Commande conversationnelle type

« Dans mon dépôt MNIN NBDA, analyse la dernière Home validée, prépare une branche avec les corrections nécessaires, exécute les contrôles open source via GitHub Actions, puis fournis les preuves et une PR brouillon. Aucun déploiement WordPress sans mon accord. »

Cette phrase utilise le plugin GitHub existant lorsque la conversation autorise ses opérations ; les scripts de CI n'ont pas d'intelligence générative propre et ne travaillent pas en permanence.

## Passage aux vrais fichiers

Le test sur les vrais fichiers de la Home reste bloqué tant que leur version approuvée et leurs médias originaux ne sont pas disponibles dans une copie privée appropriée pour l'outil d'exécution. Le rapport sur le fichier fictif ne doit jamais être présenté comme un audit du site réel.

Sources officielles :
- https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt
- https://docs.github.com/en/actions/reference/runners/github-hosted-runners
