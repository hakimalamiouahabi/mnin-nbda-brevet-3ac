# Solution réaliste — 700 agents logiques avec ChatGPT Pro et Sign in with ChatGPT

**État vérifié le 13 octobre 2026 : solution architecturale documentée, NON INSTALLÉE, NON AUTORISÉE par OAuth, et 0 instance autonome lancée.**

## Nouveau mécanisme officiel (septembre 2026)

OpenAI a publié une voie distincte de la facturation API classique :
- [OpenAI : utiliser son forfait ChatGPT dans une application compatible](https://help.openai.com/en/articles/20001542-using-your-chatgpt-plan-in-other-apps-and-sites)
- [Documentation officielle : applications open source et partage du forfait](https://developers.openai.com/siwc/token-sharing-open-source)
- [Mode d'emploi OAuth sans clé API utilisateur](https://developers.openai.com/siwc/token-sharing-open-source/sign-in)
- [Requêtes de modèle et limites](https://developers.openai.com/siwc/token-sharing-open-source/models-and-inference)
- [Limites techniques du mode préversion](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations)
- [Conditions d'utilisation (29 septembre 2026)](https://openai.com/policies/sign-in-with-chatgpt-terms/)
- [DevKit de référence OpenAI](https://github.com/openai/sign-in-with-chatgpt-devkit), **licence spécifique non commerciale** : respecter sa licence avant de copier son code.

Les applications open source compatibles peuvent recevoir **une autorisation utilisateur** pour effectuer des demandes IA éligibles avec le quota ChatGPT Plus/Pro, **sans clé API classique ni facture API séparée pour ces demandes couvertes**. Techniquement, elles utilisent l'interface Responses API officielle avec un jeton d'autorisation OAuth. C'est **une API**, mais **sans clé API facturée séparément**.

Ceci est **différent** de l'autorisation d'écriture MCP dans l'interface ChatGPT, qui conserve ses propres limites et ses propres permissions. L'accès au forfait ne donne pas automatiquement accès aux connecteurs GitHub/Cloudflare/WordPress de la conversation.

## Organisation d'exécution proposée — ne changer aucun des 700 profils

1. Charger `agents/manifest-700-target.json` (exactement 700 IDs originaux, 5 DSI, 30 senior managers, 60 managers, 60 team leaders, 545 experts).
2. Proposer un programme open source **exécuté sur l'ordinateur Windows de l'utilisateur** (ou machine qu'il contrôle) avec bouton « Continuer avec ChatGPT ». Le programme doit être entièrement open source et respecter les règles du service.
3. L'utilisateur se connecte via la page officielle OpenAI et autorise explicitement l'application à utiliser une partie de son forfait. Ne jamais demander son mot de passe ni ses cookies.
4. Un coordinateur sélectionne, selon la mission, 3–8 **profils déjà existants**. Chaque profil peut recevoir **sa propre requête au modèle** et produire une réponse distincte ; le contrôleur consolide et signale les divergences. Les 700 sont **disponibles**, pas nécessairement tous lancés ni simultanés. Le service peut limiter le débit et les demandes.
5. Prévoir une file d'attente, le suivi du quota, l'arrêt immédiat, des comptes rendus de chaque tâche, et une approbation séparée pour les opérations sensibles. L'autonomie sur les *réflexions* ne vaut pas délégation de permissions de production.
6. Sauvegarder les jetons **uniquement sous protection locale de l'utilisateur**, jamais sur GitHub public, dans des logs ou sur des runners gérés par un tiers ; conserver les sorties sans données personnelles d'élèves.
7. Ne pas utiliser le champ Responses `multi_agent` avec le partage de forfait : il est indiqué **non pris en charge** en préversion ; implémenter l'organisation de manière explicite avec plusieurs requêtes normales, idéalement limitées en nombre.

## Différence entre deux options

**A. 100 % dans les conversations ChatGPT :** actuellement opérationnel. L'assistant simule successivement des points de vue de métiers, utilise les outils connectés et fait le travail. **Pas 700 agents IA indépendants.**

**B. 700 agents logiques avec réponses individuelles :** réalisable **sous réserve de l'éligibilité et du consentement du compte** par une application open source installée sur un **appareil contrôlé par l'utilisateur**. L'application envoie des requêtes de modèle séparées utilisant le forfait ChatGPT autorisé, avec consommation de quota. **Pas encore développé, installé, authentifié ou testé.**

Une application installée localement n'implique pas un serveur payant, mais elle doit être ouverte/active pour fonctionner. Pour du 24/7 ou une exécution à distance, il faut un environnement d'exécution approprié et autorisé. Les machines éphémères GitHub Actions ne sont pas une solution de stockage sécurisé des jetons utilisateur ; ne jamais placer des jetons SIWC dans des dépôts, secrets partagés ou logs.

## Prérequis utilisateur qui ne peuvent être remplacés par un outil GitHub

- Accès physique à son appareil, ou à une machine personnelle contrôlée.
- Installation d'une application locale compatible, après revue de sa provenance et de sa licence.
- Connexion interactive **« Continuer avec ChatGPT »** et accord explicite sur le partage du forfait.
- Vérification effective qu'un modèle est disponible et qu'une requête terminée reçoit un événement `response.completed`.
- Paramétrage éventuel des limites d'utilisation sous Paramètres ChatGPT → Usage ; ne jamais activer automatiquement des crédits payants.

## Protections imposées au projet

Aucun rôle nouveau : ne créer ni changer aucun ID. Aucun secret/version de jeton dans le dépôt public. Aucune requête IA lancée ni facturation implicite au moment d'ajouter cette documentation. Aucune installation de frameworks redondants (CrewAI/LangGraph/etc.) tant que l'application minimale avec OAuth officiel n'a pas été testée. Respecter l'autorisation humaine pour l'accès aux données sensibles et les écritures WordPress/Cloudflare.

**Décision :** c'est la première solution fondée sur la documentation OpenAI qui permet d'envisager de vraies requêtes IA indépendantes par profil **avec ChatGPT Pro**, sans clé API IA payante distincte. Elle ne garantit pas l'exécution simultanée de 700 profils, ni un usage illimité, ni le fonctionnement dans toutes les conversations ChatGPT.
