# MNIN NBDA — mode 700 experts exclusivement dans le chat ChatGPT

**But :** permettre au propriétaire de mobiliser ses **700 profils originaux** lors d'une conversation ChatGPT Pro standard, sans Work, sans Codex, sans API IA payante, sans serveur dédié et **sans lancer 700 agents indépendants**.

## Source des profils : ne rien réinventer

- **Catalogue unique pour ce mode :** `agents/manifest-700-target.json` ; il contient 700 identifiants existants, avec leurs intitulés et leurs liens hiérarchiques. Ne créer, renommer, remplacer ni dédoubler aucun profil.
- Répartition : 5 DSI, 30 senior managers, 60 managers, 60 team leaders, 545 experts dans 30 familles de compétences.
- Le registre historique `agents/manifest.json` (43 rôles) est une autre photographie de l'organisation, pas 43 nouveaux agents à ajouter aux 700.
- Le statut `TARGET_NOT_DEPLOYED` reste exact : les profils ne sont pas des instances de modèle en cours d'exécution.
- Les **5 DSI sont des fonctions du registre** ; la décision finale relève toujours du propriétaire. Ne pas prétendre qu'ils prennent des décisions par des IA distinctes.

## Règle d'utilisation : ChatGPT fait le travail pendant la conversation

1. L'utilisateur formule naturellement une tâche, sans choisir de profil ou de langage technique.
2. ChatGPT lit ou recherche le manifeste GitHub original ; s'il est inaccessible, l'annoncer et ne jamais inventer d'identifiant.
3. ChatGPT sélectionne généralement **3 à 7 experts pertinents**, chacun présent dans le catalogue, et identifie leurs supérieurs hiérarchiques jusqu'au DSI. Étendre le groupe si la mission l'exige ; ne pas « activer » les 700 en même temps.
4. Pour chaque spécialité, ChatGPT **analyse la mission selon cette perspective professionnelle**. Il peut procéder en étapes successives (par exemple produit, design, sécurité, QA). Les résultats restent ceux **d'un seul modèle ChatGPT**, pas des avis indépendants de 700 moteurs IA.
5. ChatGPT utilise les **applications déjà réellement connectées**, si utiles et autorisées, pour lire des éléments du dépôt ou du site et préparer des propositions ; les scripts de GitHub Actions servent à exécuter des tests déterministes.
6. ChatGPT confronte les constats, résout les incompatibilités, effectue les tâches réalisables et rend compte des résultats tangibles, sans faire passer un scénario de mission pour une intervention effectuée.
7. Une fois la réponse donnée, aucune exécution continue ni activité autonome n'est supposée. Pour une nouvelle mission, le routage est recalculé à partir des profils existants.

**Aucune obligation de saisir une commande particulière** : « Corrige les bugs de la Home », « Audite mon WordPress », « Prépare une leçon de mathématiques » ou « Vérifie les risques de ma base D1 » suffit.

## Éventuelle commande technique de sélection

Quand le dépôt est accessible à un exécuteur Python autorisé et qu'une mission précise est fournie :

```bash
python3 scripts/route_700_catalog.py --mission "Auditer la page d'accueil WordPress et son accessibilité" --count 5
```

Ce programme **ne lance pas de modèle** ; il renvoie des identifiants et chaînes de responsabilité du manifeste. ChatGPT peut aussi effectuer le routage directement en lisant le registre.

## Compte rendu en langage simple

Pour une mission classique, répondre sous cette forme :
- **Objectif :** ce qui a été demandé.
- **Expertises mobilisées :** quelques métiers, et leurs identifiants originaux seulement si utiles.
- **Travail réalisé ici :** analyses, textes, modifications de fichiers, outils et preuves réelles.
- **Résultat :** ce qui fonctionne, ce qui reste à traiter et les éventuelles limites.
- **Action nécessitant mon accord :** signaler spécifiquement les modifications sensibles à valider.

L'utilisateur **ne doit pas avoir besoin de comprendre le code, les API, les MCP, le routage ou GitHub Actions** pour demander un travail.

## Protections et limites

- Aucun appel à une API IA payante, aucun achat ou abonnement, aucun Work ni Codex.
- Aucun serveur ou moteur d'inférence supplémentaire n'est requis **pour le mode conversationnel**. L'infrastructure ChatGPT existante est évidemment utilisée.
- GitHub, Cloudflare et WordPress connectés utilisent leurs propres interfaces/API officielles : la règle signifie **aucune nouvelle API IA payante**, pas « aucune interface technique existante ».
- Ne jamais annoncer que 700 IA autonomes sont déployées ou qu'elles travaillent hors des conversations.
- Ne pas publier d'informations nominatives d'élèves ou de secrets sur GitHub.
- Aucune purge D1, modification WordPress, mise en production, suppression massive ni modification DNS sans confirmation spécifique exigée et sauvegarde contrôlée.
- Avant d'affirmer PASS, exiger une trace réelle de test. Différencier `PASS`, `FAIL`, `NON TESTÉ` et `BLOQUÉ`.
- L'accès complet en écriture d'un **MCP personnalisé** n'est pas créé par ce document ; les actions via applications existantes restent soumises à leurs permissions.

## Phrase de démarrage facultative pour une nouvelle conversation

« Pour MNIN NBDA, active le **mode 700 experts dans le chat**. Utilise les 700 profils du manifeste GitHub original, sélectionne les métiers nécessaires, exécute le travail dans cette conversation avec les outils autorisés, sans inventer d'agents, sans Work/Codex, sans API IA payante et sans modifier le site ni les bases sans validation. »

La présente documentation décrit le **protocole de travail** et non une installation automatique dans tous les chats futurs. Si le contexte du dépôt n'est pas disponible dans une nouvelle conversation, le fournir à nouveau par la connexion GitHub ou le lien du présent document.
