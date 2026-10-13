# MNIN Bridge Pro — rétablir le mode « Équipe 700 » dans ChatGPT

Le registre d'origine se trouve dans `agents/manifest-700-target.json`. Ce guide et le script de routage ne sont **pas** une application ChatGPT installée ni un MCP déployé.

## Ce qui fonctionnera dans une conversation

1. Écrire normalement « Équipe 700 : [ce que je veux faire] » ou simplement décrire le travail.
2. Le coordinateur ChatGPT consulte le manifeste d'origine sur GitHub si l'application est disponible, ou utilise les profils fournis dans le contexte.
3. Il choisit quelques profils vérifiés, applique leurs points de vue successivement et exécute les actions permises par les applications déjà connectées.
4. Le moteur de routage `scripts/route_700_catalog.py` peut préparer une sélection, mais ne démarre **aucune IA indépendante**.

## Dépannage : « mon outil ne fonctionne plus »

- Si un programme ne choisit plus d'experts, exécuter les contrôles de la PR de réparation : le routeur comprend désormais les demandes naturelles (panne, bug, WordPress, Cloudflare, GitHub, pédagogie, visuels), avec test de non-régression.
- Si ChatGPT affiche « MNIN Bridge non disponible », c'est normal tant que le **serveur MCP personnalisé n'est pas déployé/autorisé**. Le document GitHub ne crée pas une application native. Utiliser directement l'application GitHub connectée et les outils WordPress/Cloudflare autorisés plutôt que prétendre avoir installé un serveur.
- Si une nouvelle conversation ne retrouve pas le registre, fournir ce lien ou un message « Équipe 700 : consulte mon manifeste sur GitHub, puis [mission] ». Pour les conversations régulières, les instructions d'un projet ChatGPT peuvent reprendre ce protocole ; elles n'installent pas une application globale.
- Si GitHub n'est pas connecté, ne pas inventer les identifiants. Utiliser une copie du manifeste apportée par l'utilisateur, ou annoncer cette indisponibilité.
- Si une mission n'a aucune compétence explicitement correspondante dans les 700 profils, le routeur retourne un statut sans correspondance au lieu de créer un nouveau profil.

## Contrôles

- Registre inchangé : 5 DSI, 30 seniors, 60 managers, 60 leaders, 545 experts ; 700 identifiants d'origine.
- Exécution : `python3 scripts/route_700_catalog.py --mission "Équipe 700 : mon outil ne fonctionne plus" --count 5`.
- Régression : `python3 -m unittest discover -s scripts -p "test_route_700_catalog.py" -v`.
- Statut véridique : **un assistant ChatGPT**, pas 700 IA séparées ou simultanées.
- Aucune API IA payante, aucune infrastructure dédiée, aucun Work/Codex.
- Aucune purge ni mise en production WordPress/Cloudflare ou fusion de branches sans procédure spécifique.

## Statut de correction

Cette documentation accompagne la branche de réparation isolée. Ne pas annoncer le script « réparé » sans que le test GitHub Actions correspondant ait effectivement réussi.

### Branche de référence pour cette PR
La réparation est comparée à `proposal/organization-700`, qui contient le registre d'origine. Les validations GitHub ne doivent pas exiger la fusion d'une autre PR de développement, encore modifiable, pour être déclenchées.
