# MNIN Bridge Pro v0.4 — suite premium pour ChatGPT Pro standard

**Statut réel au 12 octobre 2026 : code en branche GitHub d'essai, non déployé, non connecté à ChatGPT, aucun plugin WordPress installé, aucune exécution autonome.**

## Périmètre
Une application MCP centrale **MNIN Bridge Pro** et dix modules de planification vérifiables :
1. Direction artistique premium.
2. Design system et composants.
3. Architecture WordPress thème + plugin métier.
4. Responsive mobile, français et arabe RTL.
5. Images, logos SVG et contrôle des originaux haute définition.
6. Ingénierie pédagogique et gouvernance de données.
7. Accessibilité et inclusion.
8. Performance Web et SEO.
9. Cybersécurité et protection des données.
10. QA et livraison contrôlée.

Ces « modules » ne sont PAS dix apps ChatGPT publiées : un seul prototype de serveur MCP expose leur catalogue, le planificateur et les conditions de délégation. L'intelligence sémantique vient du modèle dans le chat ; le routage local est déterministe. Les 43 rôles experts existants sont sélectionnés pour chaque tâche ; **aucune instance d'agent n'est lancée par ce code**.

## Outils MCP ajoutés en v0.4
- `bridge_premium_modules()` : inventaire de dix modules, profils concernés et preuves exigées.
- `bridge_plan_premium_task(task, selected_modules?)` : plan de travail borné, sans exécution.
- `bridge_explain_owner_delegation(action)` : classement des autorisations permanentes, par action, ou refus. Aucun pouvoir d'autorisation.

## Délégation permanente du propriétaire
Le fichier `owner_delegation_policy.json` enregistre la **préférence de délégation maximale** du propriétaire, sans redemander pour les missions courantes admissibles : inventaire et vérification des assets, préparation de missions, rapports, QA isolée et écritures sur branches non principales. Cela vaut seulement **dans la limite des permissions authentifiées réellement obtenues et des coûts zéro**.

Il ne constitue PAS une preuve OAuth, une identité vérifiée, un accord de facturation, une preuve du forfait Pro, ni une dérogation aux validations obligatoires de ChatGPT ou des fournisseurs tiers.

Toute écriture WordPress (staging compris), publication, fusion vers `main`, DNS, facture, export de données privées, suppression massive et modification de permissions exige une approbation distincte. L'export de secrets ou de données de mineurs n'est pas réalisable avec ces seules instructions.

## Particularités ChatGPT Pro
- Surface cible : ChatGPT **standard** uniquement ; Work et Codex exclus du projet.
- La disponibilité complète des actions d'écriture sur MCP personnalisé dépend du forfait et de la plateforme. En cas d'absence de preuve fiable de forfait et de surface, **aucun contrôle de type « Pro seulement » ne doit être déclaré opérationnel**.
- Les apps GitHub, WordPress.com, WPVibe, MagicPath et autres apps tierces utilisables depuis le chat sont indépendantes de ce serveur MCP et conservent leurs propres permissions.
- Un manifeste en dépôt n'installe pas automatiquement l'application dans ChatGPT. L'hébergement HTTPS, l'authentification, l'autorisation de connexion et le test restent à faire via les mécanismes réels de la plateforme.

## Contrôles qualité pour le site MNIN NBDA
- Reproduction fidèle de la Home approuvée, sans inventer de références.
- Responsive multi-écrans, contrôle clavier, direction RTL et localisation.
- Les SVG sont vectoriels : « 8K » n'est pas une caractéristique pertinente pour eux. Les images raster doivent être vérifiées à la résolution native et selon la taille d'affichage ; ne pas agrandir artificiellement des sources pauvres.
- Chaque résultat observé porte la preuve de l'essai ; état PASS, FAIL, NON TESTÉ ou BLOQUÉ.
- Aucun média original privé, token ou donnée personnelle d'élève dans GitHub : le dépôt est **public** selon la lecture GitHub d'octobre 2026.

## Essais et activation
Tests unitaires ajoutés dans `mnin-bridge/tests/test_premium_suite.py`. À exécuter localement depuis la racine du dépôt :
```sh
python3 -m unittest discover -s mnin-bridge/tests -v
```
**Ne pas déclarer PASS avant une exécution observée.**

Le serveur MCP conserve `MNIN_ENABLE_DISPATCH=0`. Il ne doit pas être exposé à internet sans authentification indépendante, protections réseau, stockage privé et revue de sécurité. Aucune API IA payante, dépense nouvelle ni mutation WordPress n'est autorisée par le prototype.

Références publiques OpenAI : 
- https://help.openai.com/en/articles/12515353-build-with-the-apps-sdk
- https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt
