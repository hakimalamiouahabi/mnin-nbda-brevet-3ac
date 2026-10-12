# Consignes centrales — MNIN NBDA / Work / Codex

## Priorités de sources
1. Dernières validations explicites du propriétaire : identité visuelle et fonctionnalités.
2. docs/references/PROMPT_MASTER_HOME_DESKTOP_XL_2026-10-11.md : mise en page et contenus de la Home spécifiés à cette date.
3. docs/references/PROMPT_MASTER_WORDPRESS_V4_2.md : exigences techniques et pédagogiques V4.2.
4. État réel du WordPress existant, contrôlé sans modification.
En cas de contradiction : consigner dans docs/STATUS.md et docs/DECISIONS.md si créé ; ne pas inventer une réponse. La dernière maquette graphique sous forme d'image n'a pas encore été ajoutée à ce dépôt.

## Huit rôles organisés par le DSI
| ID | Rôle | Instruction |
|---|---|---|
| DSI | Directeur SI (orchestrateur) | agents/01-directeur-si.md |
| DATA_ENG | Data Engineering | agents/02-data-engineering.md |
| DATA_SCI | Data Scientist | agents/03-data-science.md |
| DATA_ANALYST | Data Analyst | agents/04-data-analyst.md |
| AI_ENG | IA Engineering | agents/05-ia-engineering.md |
| WEB_DEV | Développement web WordPress | agents/06-developpement-web.md |
| DESIGN_CONTENT | Design & Content Creator | agents/07-design-content.md |
| DEVOPS | DevOps / Intégration | agents/08-devops.md |

Lire agents/manifest.json et docs/AGENT_OPERATING_MODEL.md. Les rôles sont des **instructions opérationnelles pour Work / Codex**, et ne garantissent pas huit agents exécutés séparément en continu.

## Principes non négociables
- Aucune API IA payante, aucun wallet, aucune clé dans le dépôt ni sur WordPress.
- Coût obligatoire supplémentaire : zéro dans l'architecture cible ; vérifier les quotas Github Actions et le forfait existant.
- Site WordPress existant : thème actif MNIN NBDA V4, aucune écriture, installation ni déploiement avant audit, sauvegarde et autorisation explicite.
- Priorité accueil conforme à la dernière maquette approuvée, aucun bloc matières sur la Home ; responsive, français/arabe, RTL.
- Architecture : thème mnin-nbda-theme + plugin métier séparé mnin-nbda-core ; Polylang Free facultatif ; pas de Tutor LMS/Elementor obligatoire.
- Protection des mineurs : minimisation, séparation foyer, aucun export de données réelles ni publication dans Git.
- Contrôles qualité réels ; seul résultat permis PASS, FAIL, NON TESTÉ ou BLOQUÉ.
- Pour une fonction IA pédagogique, chemin déterministe sans IA obligatoire ; aucune IA distante exigée.
- Changement de DNS, paiement, production, données réelles, thème et extensions actifs : autorisation humaine explicite.

## Procédure commune
1. DSI : vérifier état, contraintes, sources et tâche précise.
2. Activer seulement les rôles pertinents pour cette tâche (pas les huit systématiquement).
3. Chaque rôle fournit un livrable vérifiable avec son contexte, preuve et limites.
4. Développement produit du code versionné ; DevOps contrôle les tests ; DSI valide les critères.
5. Rapporter les blocages et la prochaine action dans docs/STATUS.md.
6. GitHub Actions n'est pas un agent IA et n'installe rien automatiquement sur WordPress.

## Terminé signifie
Code réellement construit, tests réellement exécutés et documentés, absence d'anomalie bloquante, conformité au master + à la maquette vérifiée, validation expresse du propriétaire avant publication.
