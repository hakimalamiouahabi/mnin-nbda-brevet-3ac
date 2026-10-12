# MNIN Bridge Pro 0.5 — démarrage exclusivement en chat standard

**12 octobre 2026 — code de prototype, non connecté en tant que plugin personnalisé.**

## Objectif produit
Piloter le site WordPress premium MNIN NBDA en français/arabe RTL et gérer design, source, QA, accessibilité, performance, confidentialité, contenus éducatifs et releases. Utiliser **le modèle ChatGPT Pro dans le chat standard** comme moteur de raisonnement ; jamais Work, jamais Codex, jamais une API IA facturée.

## Réalité technique vérifiée
- **43 profils** définis dans `agents/manifest.json` : 1 DSI, 3 seniors, 3 managers, 6 leaders et 30 experts. Le runtime ne lance aucun agent autonome.
- **10 modules** dans `premium_suite.py`, qui produisent des plans ou des inventaires.
- **4 workflows structurés** dans `agent_conductor.py` : `premium_home`, `wordpress_feature`, `asset_quality`, `educational_module`. Chaque étape comporte une chaîne DSI → expert, une dépendance, une preuve attendue, et `NON TESTÉ` au départ.
- **6 outils de planification** ajoutés en versions 0.4/0.5 au serveur MCP : catalogue premium, plan premium, interprétation de la délégation, organigramme réel, mission DSI, statut d'éligibilité Pro.
- **Aucune action d'écriture exposée par ces six outils.** Les opérations préexistantes de programmation ou QA restent désactivées et le serveur n'est pas connecté.
- Le dépôt GitHub a été observé **PUBLIC**. N'y placer aucun original privé, secret, donnée nominative de mineur, ni jeton.

## Délégation demandée
La politique `owner_delegation_policy.json` contient :
- `owner_instructions_permanent: true` ; `mode: MAXIMUM_CONTINUING_DELEGATION_WITHIN_VERIFIED_PERMISSIONS` ;
- actions ordinaires planifiées sans revalidation répétitive, si les applications autorisent l'opération et si la limite de coût est zéro ;
- catégories gardées à approbation spécifique : WordPress live, fusion principale, dépenses, changement DNS ou droits, exports privés, suppressions massives et autres opérations sensibles ;
- refus du contournement OAuth, de la désactivation des journaux de sécurité ou des protections de la plateforme.

Ce paramétrage enregistre **une préférence permanente et révocable**, pas une procuration OAuth permanente ni une capacité de contrôle total de ChatGPT.

## « ChatGPT Pro uniquement »
Le serveur documente la cible `target_subscription: Pro` et `target_surface: standard_chat_only`. **La plateforme ne transmet pas nécessairement d'attestation fiable du forfait ou du mode de conversation au serveur** ; par défaut, `subscription_gate_readiness()` retourne `BLOQUÉ`, sans privilège. Un simple texte `"Pro": true` fourni au modèle n'a aucune valeur d'authentification.

OpenAI documente actuellement le mode développeur MCP pour Pro en lecture/fetch, et réserve les permissions complètes de modification/écriture MCP aux forfaits Business/Enterprise/Edu. Les plugins tiers déjà installés (GitHub, WPVibe, WordPress.com, MagicPath) restent indépendants et peuvent disposer de leurs propres actions selon les permissions effectivement accordées.

Sources :
- https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt
- https://developers.openai.com/plugins/build/auth
- https://developers.openai.com/plugins/build/mcp-server

## Exécution sur le chat standard, sans plugin encore déployé
1. Employer directement les apps connectées pour les **actions autorisées**, notamment GitHub et WordPress.com, avec les contrôles fournisseurs.
2. Pour chaque nouveau chantier, suivre `mnin-bridge/skills/chatgpt-pro/SKILL.md` ; mettre les changements de code en branches `feature/*` ou `proposal/*`.
3. Vérifier les mesures réellement observées : images non pixellisées, mobile/desktop, FR/AR RTL, contrastes, clavier, Core Web Vitals sans score inventé.
4. Produire une PR en brouillon avec diffs, tests vérifiés et plan de réversibilité ; pas de fusion automatique ou de WordPress modifié implicitement.
5. Ne pas présenter 700 fiches de rôles ou 43 fiches de rôles comme des exécutions concurrentes.

## Contrôle automatisé sur GitHub
Le workflow `.github/workflows/validation.yml` lance désormais :
```sh
python3 scripts/validate_workspace.py
python3 -m compileall -q mnin-bridge
python3 -m unittest discover -s mnin-bridge/tests -v
```
Tests sur runner standard public GitHub `ubuntu-latest`. La politique GitHub actuelle décrit ce runner comme gratuit sur les dépôts publics : https://docs.github.com/en/billing/concepts/product-billing/github-actions.

**Un commit qui ajoute les tests ne vaut PAS résultat PASS.** Consulter le run GitHub réel et son conclusion/commit avant toute déclaration de succès.

## Prochaine étape d'infrastructure
Afin de connecter un MCP personnalisé : endpoint distant HTTPS, OAuth 2.1 conforme MCP, identité vérifiable, sécurisation des assets privés, protection de l'origine et des sorties, audit de sécurité. Aucun hébergeur payant ni nouvelle identité n'est configuré automatiquement. La compatibilité stricte Pro-only ne pourra être affirmée qu'avec une attestation fiable.
