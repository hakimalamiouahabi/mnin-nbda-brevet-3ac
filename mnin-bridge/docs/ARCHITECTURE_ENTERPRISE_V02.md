# MNIN Bridge — architecture d'entreprise V0.2 (proposition exécutable par étapes)

**Statut : PROTOTYPE — NON DÉPLOYÉ, NON CONNECTÉ, aucun agent lancé par le plugin.**

## Vision et limites

Créer une plateforme d'exécution MCP propre à MNIN NBDA, afin d'offrir à ChatGPT des outils spécialisés :
gestion des binaires, code, tests réels, captures pleine page, QA visuelle, WordPress, orchestration et rapports.

L'ajout d'outils ne crée pas un accès illimité à Codex, ChatGPT Work, aux appareils ni à des comptes externes. Chaque capacité dépend de services réellement connectés, de ressources de calcul, de permissions et d'une politique de coûts.

## Architecture cible

```text
Utilisateur propriétaire
   |
   v
ChatGPT / Plugin MCP -- HTTPS + OAuth 2.1, JWT validé pour chaque appel
   |
   v
MNIN Bridge API (scope par outil ; identity-bound)
   |---- catalogue de capacités [V0.2]
   |---- planificateur de missions + journaux SQLite [V0.2]
   |---- coffre privé de binaires et contrôle SHA256 [V0.1 local]
   |---- connecteur GitHub limité en lecture [V0.1 local]
   |---- adaptateur d'approbations indépendantes [À FAIRE]
   |---- ordonnanceur à limites de parallélisme [À FAIRE]
   |
   +---- workers isolés [À FAIRE / non démarrés]
        |-- BrowserLab : 21 viewports, captures et validations
        |-- AssetLab : vector/HD, densité, manifest et provenance
        |-- CodeLab : tests, revue de diff, PHP/JS/TS, SAST
        |-- 3DLab : validation GLB, FPS et fallback statique
        |-- WP ReadOps : inventaire WordPress en lecture seule
        |-- DataLab : sources pédagogiques et gouvernance
        |-- EduLab : séquences 1AC/2AC/3AC avec contrôle humain
        |-- ReleaseLab : ZIP, staging isolé, rollback testé
```

## Capacités en code

| Capacité | Statut | Exécutable depuis ChatGPT aujourd'hui ? |
|---|---|---|
| Catalogue de missions et compétences | Code V0.2 | Non, plugin non connecté |
| Contrôle des paramètres (liste blanche) | Code V0.2 | Non, plugin non connecté |
| Planification persistante de missions | Code V0.2 | Non, plugin non connecté |
| Journal d'événements missions | Code V0.2 | Non, plugin non connecté |
| SHA-256 sur original privé | Code V0.1 | Non, serveur non configuré |
| Suivi factuel d'un workflow GitHub | Code V0.1 | Non, credentials non configurés |
| Captures navigateur pilote (5 formats) | Code V0.1 | Non, worker non exécuté |
| Captures automatisées de 21 formats | À développer | Non |
| Amine 3D Blender/Three.js | À développer | Non |
| Écriture WordPress | Interdite par défaut | Non |
| 700 agents en permanence | Ni implémenté ni garanti | Non |

Les 700 profils de `agents/manifest-700-target.json` sont sur une autre branche de proposition. Leur existence ne prouve aucun runtime.

## Politique de permissions

- `READ` : inventaire et consultations scopées à l'utilisateur authentifié.
- `PLAN` : missions préparées, **aucune exécution**.
- `RUN_QA` : job isolé, limite de budget, version Git et source prévalidées ; approbation serveur réelle.
- `WRITE_BRANCH` : uniquement dans `feature/*`, diff proposé, revision humaine.
- `WORDPRESS_STAGING_WRITE` : séparé, désactivé jusqu'à preuve de sauvegarde, rollback et approbation explicite.
- `PRODUCTION_WRITE` : hors périmètre de l'activation initiale.

Aucune commande shell arbitraire depuis un modèle. Aucun token administrateur dans le dépôt ou dans les invites. Pas d'asset privé dans GitHub public. Ne jamais confondre booléen `approved=true` envoyé par le modèle et preuve de consentement utilisateur : l'approbation doit être reçue **hors du canal d'outil du modèle**, vérifiée et liée au job exact.

## Livraison incrémentale

**G0 :** identifier fournisseur OAuth, dépôt privé/public, stockage des assets, quotas et hébergement 0 frais supplémentaires vérifiés.

**G1 :** tests unitaires sur le code existant, analyse sécurité, vérification manifest plugin, aucun accès WordPress.

**G2 :** service MCP privé accessible par HTTPS avec OAuth 2.1 et profils scopes, tests MCP Inspector.

**G3 :** un cycle complet (original PNG → empreinte → HTML sous branche → QA navigateur → vraies captures → rapport).

**G4 :** 21 viewports, performance, accessibilité, fidélité graphique, assets haute définition.

**G5 :** ordonnanceur de sous-agents avec limites, preuves et coût réel, puis fonctions de développement plus larges si elles apportent du gain mesuré.

**G6 :** intégrations WordPress seulement après validation humaine spécifique.

## Mesures d'efficacité

Comparer les temps de livraison d'une vraie page responsive, le nombre d'écarts visuels, le taux d'erreurs, les retours manuels, le temps de revue, la consommation de ressources et la conformité. Aucun gain linéaire n'est présumé en passant de 43 à 700 rôles.
