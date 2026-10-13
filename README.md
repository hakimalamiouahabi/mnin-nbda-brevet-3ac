# MNIN NBDA — utilisation des 700 experts exclusivement dans ChatGPT

**Pour utiliser les 700 profils existants directement dans une conversation ChatGPT Pro standard, sans Work, Codex ni API IA payante :** lire [MODE 700 EXPERTS DANS LE CHAT](docs/CHAT_ONLY_700.md).

Il suffit d'écrire sa mission en langage naturel. ChatGPT sélectionne les profils pertinents à partir de `agents/manifest-700-target.json` et effectue le travail pendant la conversation. Aucune IA séparée ni activité permanente n'est lancée. Le registre historique de 43 rôles documenté plus bas reste conservé sans créer de profils supplémentaires.

---

# MNIN NBDA — organisation de 43 profils IA spécialisés

Configuration GitHub de la structure demandée pour développer la plateforme WordPress MNIN NBDA **sans API IA payante**.

| Niveau | Effectif |
|---|---:|
| Directeur SI | 1 |
| Senior Managers | 3 |
| Managers | 3 |
| Team Leaders | 6 |
| Agents experts | 30 |
| **Total** | **43** |

## Référentiel
- `agents/manifest.json` : identifiants, liens hiérarchiques et 43 instructions référencées.
- `agents/org-structure.json` : organigramme imbriqué en trois portefeuilles et six équipes de cinq spécialistes.
- `agents/01-directeur-si.md` : orchestration générale.
- `agents/leadership/` : 12 profils d'encadrement.
- `agents/02-*.md` à `agents/31-*.md` : 30 spécialistes.
- `AGENTS.md`, `docs/AGENT_OPERATING_MODEL.md` : règles de travail.
- `docs/WORK_MASTER_START.md` : instructions à donner dans ChatGPT Work.
- `docs/ROADMAP.md`, `docs/STATUS.md` : étapes et preuves.
- `docs/references/` : Prompt Master V4.2 et Home Desktop XL.

## Répartition
**Produit :** Product/EdTech + Design/Contenus.

**Ingénierie :** Plateforme Web + Data/IA.

**Exploitation :** QA/Sécurité + DevOps/Livraison.

## Démarrage
Ouvrir Work, connecter le dépôt GitHub autorisé et faire lire `docs/WORK_MASTER_START.md` au rôle DSI. Celui-ci commence par les tickets #1 à #3 en audit **sans écriture sur WordPress**.

## Statut réel
Les 43 **descriptions de rôles** sont enregistrées dans GitHub. Aucun déploiement de 43 instances IA parallèles, aucune planification permanente ni travail en arrière-plan Work n'a été activé par ces fichiers. Aucun code de WordPress n'est présumé développé ou testé sur cette seule base. Les comptes GitHub Actions et Work/Codex restent soumis à leurs limitations et droits.
