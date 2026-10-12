# Instructions centrales — MNIN NBDA / ChatGPT Work / Codex

## Architecture organisationnelle figée
**43 profils documentés : 1 Directeur SI + 3 Senior Managers + 3 Managers + 6 Team Leaders + 30 agents spécialistes.**
La hiérarchie et toutes les affectations se trouvent dans `agents/manifest.json` (référence normative) et `agents/org-structure.json` (arbre de lecture). Ne jamais interpréter 43 profils comme 43 agents IA autonomes réellement lancés.

### Chaîne de responsabilité
**Propriétaire → DSI → Senior Manager → Manager → Team Leader → Expert.**
Le DSI arbitre les conflits et contrôle l'architecture, les coûts, les risques et les autorisations. Chaque Senior Manager supervise un Manager, chaque Manager deux Team Leaders, chaque Team Leader cinq spécialistes. Le Team Leader évite l'activation simultanée des cinq agents lorsqu'ils ne sont pas pertinents.

### Portefeuilles
- Produit & pédagogie : `SM_PRODUCT` → `M_PRODUCT` → `TL_PRODUCT_EDTECH`, `TL_DESIGN_CONTENT`.
- Ingénierie & données : `SM_ENGINEERING` → `M_ENGINEERING` → `TL_WEB_PLATFORM`, `TL_DATA_AI`.
- Qualité & exploitation : `SM_TRUST` → `M_DELIVERY` → `TL_QA_SECURITY`, `TL_DEVOPS_RELEASE`.

## Autorité documentaire
1. Dernières décisions explicitement validées par le propriétaire.
2. `docs/references/PROMPT_MASTER_HOME_DESKTOP_XL_2026-10-11.md` concernant la Home.
3. `docs/references/PROMPT_MASTER_WORDPRESS_V4_2.md` concernant le socle produit et technique.
4. Observation factuelle en lecture seule du site WordPress existant.
Un conflit ne peut pas être résolu par supposition. La référence visuelle originale doit être disponible pour garantir une reproduction fidèle.

## Restrictions absolues
- Aucune API IA payante ; aucune dépense ou abonnement ajouté sans accord.
- Aucune installation d'extension WordPress, écriture sur le site, publication ou changement DNS sans autorisation explicite.
- Le site WordPress MNIN NBDA V4 existant ne doit jamais être écrasé avant audit et sauvegarde vérifiables.
- Design : Home d'abord, conforme à la maquette approuvée, sans bloc de matières ; puis déclinaisons responsive FR/AR RTL.
- Architecture WordPress : thème indépendant `mnin-nbda-theme` + plugin métier `mnin-nbda-core`. Tutor LMS et Elementor non obligatoires ; Polylang Free optionnel.
- Collecte minimale sur les mineurs : jamais de données réelles dans GitHub, jamais de transmission non autorisée à une IA.
- Tests : statut `PASS`, `FAIL`, `NON TESTÉ` ou `BLOQUÉ` ; ne jamais déclarer testé ce qui ne l'est pas.
- AI Engineering : optionnel pour l'usage du site ; aucun modèle distant nécessaire à son fonctionnement essentiel.

## Protocole de travail
Le DSI choisit une tâche du backlog, l'attribue à un Senior Manager, puis Manager et Team Leader concernés ; celui-ci mobilise le ou les spécialistes pertinents. Chaque transfert doit mentionner ID, propriétaire, entrées, critères d'acceptation, fichier/commit, résultats et blocages. Qualité & DevOps interviennent sur toute livraison sensible avant validation du DSI.

## Autonomie effective
Ces profils sont des **prompts spécialisés dans un dépôt privé**, et non des processus persistants. Work/Codex doivent être déclenchés/configurés séparément pour les exécuter, séquentiellement au besoin. GitHub Actions lance uniquement des tests déterministes : pas de 43 modèles IA ni de garantie 24 h/24.

## Fin de tâche
Un objectif n'est clos qu'après code livré lorsque requis, tests exécutés et documentés, contrôle des risques, conformité au master, et validation humaine avant tout déploiement.
