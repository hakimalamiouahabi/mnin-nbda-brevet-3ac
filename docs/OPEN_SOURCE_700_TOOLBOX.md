# Boîte à outils open source vérifiée — Équipe 700
Dernière revue : 13 octobre 2026. **Un lien GitHub n'est pas une connexion active ni une installation.**

## Principes
- Conserver les **700 profils exactement** dans `agents/manifest-700-target.json` ; ne créer aucun agent supplémentaire.
- L'IA utilisée dans les conversations reste **ChatGPT Pro**, avec les applications déjà connectées et leurs limites. Une bibliothèque d'agents ne partage pas automatiquement le moteur ChatGPT Pro hors du chat et ne donne pas 700 modèles indépendants.
- **Zéro API d'inférence IA payante**, pas de serveur dédié, pas d'abonnement supplémentaire, pas de Work ni Codex pour cette boîte à outils.
- Le dépôt est public : **jamais de clé, de données personnelles ou de données d'élèves dans les fichiers ou les logs**.
- Pas de modifications WordPress/Cloudflare ni de purge automatisée ; lecture seule par défaut, revue explicite des interventions sensibles.
- Versions des outils exécutés verrouillées ; CI `contents: read`. Aucune instruction inconnue tirée d'un dépôt tiers ne remplace nos règles de sécurité.

## A. Opérationnels dans le dépôt GitHub après validation du workflow
Les binaires sont **installés uniquement sur la machine éphémère GitHub Actions**, pas dans l'interface ChatGPT ni sur WordPress.

| Outil libre | Utilisation concrète | Licence | Installation |
| --- | --- | --- | --- |
| [Ruff](https://github.com/astral-sh/ruff) | Détecter erreurs Python et imports inutilisés | MIT | Workflow `oss-toolbox-audit.yml`, version 0.17.0 |
| [Bandit](https://github.com/PyCQA/bandit) | Détecter certaines erreurs de sécurité dans les scripts | Apache-2.0 | Workflow, version 1.9.4 |
| [Zizmor](https://github.com/zizmorcore/zizmor) | Auditer la sécurité des fichiers GitHub Actions | MIT | Workflow, version 1.30.1, **offline** |
| [Python unittest](https://docs.python.org/3/library/unittest.html) | Vérifier le routage des **700 identifiants originaux** | Bibliothèque standard Python | Déjà opérationnel dans `validate-700-catalog.yml` |

**Preuve d'exécution :** consulter les contrôles de la proposition GitHub n°19. Ne déclarer les outils opérationnels qu'après résultat `success` de `oss-toolbox-audit.yml`. Les audits statiques ne prouvent pas l'absence de vulnérabilités.

## B. Connecteurs officiels disponibles / à évaluer

| Projet public | Usage | Statut exact pour ce projet |
| --- | --- | --- |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | Dépôts, issues, PR, actions | **Application GitHub déjà connectée** ; serveur OSS distinct non installé |
| [Cloudflare MCP](https://github.com/cloudflare/mcp) | Cloudflare API via MCP | **Application Cloudflare V1 déjà connectée** ; paquet source distinct non installé |
| [WordPress MCP Adapter](https://github.com/WordPress/mcp-adapter) | Expose WordPress Abilities via MCP, GPL-2.0+ | **Application WordPress.com déjà connectée** ; adaptateur non installé et non requis pour les actions disponibles |
| [WP-CLI](https://github.com/wp-cli/wp-cli) | Administration WordPress depuis un terminal, MIT | Non installé. Demande un environnement et un accès WordPress compatible ; ne pas lancer sur prod |
| [MCP reference servers](https://github.com/modelcontextprotocol/servers) | Exemples et implémentations du protocole | **Référence évaluée**, pas un serveur installé dans ChatGPT |
| [actionlint](https://github.com/rhysd/actionlint) | Validation approfondie des workflows GitHub | Référence pour une future étape ; non installé |
| [pip-audit](https://github.com/pypa/pip-audit) | Audit vulnérabilités des dépendances Python | Référence pour quand des dépendances applicatives seront présentes ; non installé |

## C. Frameworks d'agents IA libres — évalués, pas connectés à ChatGPT Pro

| Projet | Licence du cœur | Bénéfice possible | Limite à respecter |
| --- | --- | --- | --- |
| [CrewAI](https://github.com/crewAIInc/crewAI) | MIT | Orchestration d'équipes et de rôles | Besoin d'un modèle d'IA + d'un exécuteur ; pas 700 instances offertes par ChatGPT |
| [LangGraph](https://github.com/langchain-ai/langgraph) | MIT | Coordination avec étapes, état et validations | Infrastructure d'exécution et fournisseur d'inférence nécessaires hors chat |
| [Smolagents](https://github.com/huggingface/smolagents) | Apache-2.0 | Agents simples et outils Python | Ne fournit pas automatiquement un modèle d'IA gratuit |
| [PydanticAI](https://github.com/pydantic/pydantic-ai) | MIT | Agents typés, tests et garde-fous | Pas d'accès automatique au moteur ChatGPT Pro |
| [Google ADK](https://github.com/google/adk-python) | Apache-2.0 | Workflows multi-agents | Nécessite un modèle et un environnement d'exécution |
| [Microsoft AutoGen](https://github.com/microsoft/autogen) | MIT pour ses composants examinés | Dialogues d'agents et orchestrations | Le SDK ne transforme pas le forfait ChatGPT en API IA gratuite |

**Décision pour les 700 existants :** ne pas installer tous ces frameworks. Ils se chevauchent et élargissent l'exposition aux dépendances sans répondre à l'exigence d'utiliser **ChatGPT Pro uniquement dans le chat**. Le protocole `docs/CHAT_700_MASTER.md` et le routeur local suffisent pour le routage des compétences, ChatGPT effectuant le raisonnement pendant la session.

## Mode d'emploi non technique
Dire dans ChatGPT : « Équipe 700, vérifie mon site WordPress et mon dépôt, montre les anomalies et propose des corrections sans rien supprimer ». Le coordinateur consulte le manifeste original, choisit les expertises et utilise les outils ChatGPT disponibles. Le workflow GitHub permet en plus de contrôler le code, **sans lancer de nouveaux moteurs d'IA**.

## Sources officielles vérifiées et limites de ChatGPT Pro
- [Mode développeur et MCP — OpenAI](https://help.openai.com/en/articles/12584461-developer-mode-and-mcp-apps-in-chatgpt) : les fonctions complètes d'écriture des **MCP personnalisés** ne sont pas débloquées sur Pro par le téléchargement d'une bibliothèque open source ; les apps existantes sont un canal distinct et disposent de leurs propres permissions.
- [Dépôt Ruff](https://github.com/astral-sh/ruff), [Bandit](https://github.com/PyCQA/bandit), [Zizmor](https://github.com/zizmorcore/zizmor) : documentations et licences publiées.
- Pas de connexion OAuth, app ChatGPT ou installation implicite lors de la simple création de ce document.
