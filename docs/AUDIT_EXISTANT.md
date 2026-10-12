# Audit non destructif MNIN NBDA — 12 octobre 2026

## Mandat et exécution
Objectif : démarrer la coordination des 43 profils sous le DSI et établir les preuves avant développement.
Snapshot GitHub : commit 2648716caeae74c80d76594cd81d47157b08977e, main.
Lecture : WORK_MASTER_START, AGENTS, manifest, organigramme, modèle, STATUS, ROADMAP et masters.
Exécution réelle : coordinateur principal DSI et deux sous-agents temporaires (DevOps, Design). Les niveaux de management sont appliqués comme responsabilités, pas comme processus distincts. La chaîne Web est exécutée dans la session principale. Aucun runtime permanent de 43 agents ni tâche récurrente configuré.

| Mission | Propriétaire hiérarchique | Spécialistes mobilisés | Résultat |
|---|---|---|---|
| AUD-03 / ticket #3 | DSI → SM_TRUST → M_DELIVERY → TL_DEVOPS_RELEASE | DEVOPS | Structure PASS ; CI courante NON TESTÉ |
| AUD-02 / ticket #2 | DSI → SM_PRODUCT → M_PRODUCT → TL_DESIGN_CONTENT | DESIGN_CONTENT | Masters inventoriés ; fidélité NON TESTÉ |
| AUD-01 / ticket #1 | DSI → SM_ENGINEERING → M_ENGINEERING → TL_WEB_PLATFORM | WP_ARCHITECT, WEB_DEV (rôles séquentiels du coordinateur) | Inventaire WordPress partiel ; sources BLOQUÉ |

## Preuves WordPress en lecture seule
Site confirmé : intellego718821273.wpcomstaging.com, ID 183190850, plateforme Atomic.
Thème actif : MNIN NBDA V4, stylesheet mnin-nbda ; thème classique, is_block_theme=false, block_templates=false, block_template_parts=false ; global_styles_id=85.
templates.list et theme.presets retournent des collections vides. Cela ne prouve pas l'absence de templates PHP ni de styles CSS.
plugins.list, source live : 11 extensions, 8 actives, 3 inactives, aucune mise à jour signalée.
Actives : Akismet 5.7.2, CoBlocks 3.1.17, Gravatar Enhanced 0.13.1, Gutenberg 24.1.0, Jetpack 16.3, Layout Grid 1.8.5, Page Optimize 0.6.3, WordPress Agent 7.9.18.
Inactives : Classic Editor 1.7.0, Crowdsignal Dashboard 3.1.8, Crowdsignal Forms 1.8.3.
mnin-nbda-core et Polylang ne figurent pas dans cette liste ; aucune conclusion sur les mu-plugins ou du code incorporé au thème.
pages.list status any : une page ID 86, accueil-darija, draft, « Accueil Darija — prévisualisation ». pages.get : content vide, template page-home-darija.php. Ne pas confondre contenu vide et rendu vide.
media.list : zéro pièce jointe retournée ; cela n'exclut pas les assets dans le thème.
settings.get : show_on_front=posts, page_on_front=0, page_for_posts=0, site_logo=0, site_icon=0, permalink /%year%/%monthnum%/%day%/%postname%/.
Confidentialité contradictoire : user_sites is_private=false, is_site_launched=false ; settings.get is_private=true, blog_public=-1. Ne pas trancher silencieusement.
Observation navigateur de la racine : « MNIN BDA », « À venir prochainement », lien Connexion. Aucun rendu de la Home inspecté ; aucune connexion ni publication effectuée.

## Inventaire de conservation
| Élément existant | Emplacement | À conserver | À migrer | À supprimer | Risque | Action |
|---|---|---|---|---|---|---|
| Thème V4 | WordPress, mnin-nbda | Oui en attendant audit | À déterminer | Non autorisé | Sources non accessibles dans les lectures effectuées | Obtenir export/source en lecture seule |
| Page Darija | ID 86, brouillon | Oui | À déterminer | Non autorisé | Template PHP non inspecté | Conserver brouillon et auditer template |
| Extensions | Inventaire live | Oui provisoirement | À déterminer | Non autorisé | Dépendances du thème inconnues | Cartographier usages avant changement |
| Médias | Collection vide | Assets du thème à inventorier | À déterminer | Non autorisé | Pièces jointes ≠ assets du thème | Inspecter fichiers exportés |
| Réglages | Lecture, identité, confidentialité | Oui | À déterminer | Non autorisé | Réponses confidentialité contradictoires | Vérifier état effectif sans écriture |
| Données élèves/foyers | Non inspectées | Aucune décision de suppression | À déterminer | Non autorisé | Données personnelles hors périmètre | Audit schéma/droits sans données réelles |

## Sauvegarde et rollback
backup.rewind_status : state=active, 3 sauvegardes ; dernière sauvegarde déclarée 2026-10-11 16:52:55, dernière tentative 16:52:57, status=finished, last_attempt_failed=false, backup_in_progress=false. Fuseau non précisé par la réponse. restore_preflight_status=null.
Sauvegarde déclarée par le fournisseur ; aucun export téléchargé ni test de restauration réalisé.
Protocole avant intervention : identifier point de restauration/version, obtenir copie vérifiable du thème et données nécessaires, définir restauration sur environnement isolé puis test autorisé. Toute restauration ou modification WordPress requiert validation explicite. Rollback : NON TESTÉ.

## GitHub et contrôles
Tickets #1, #2, #3 ouverts ; aucun ticket clôturé.
python3 scripts/validate_workspace.py sur copie locale du commit : exit 0, PASS 43 profils et hiérarchie ; PHP NON TESTÉ (aucun fichier PHP).
Contrôle indépendant DevOps : liens parents/enfants et chemins manifest/arbre cohérents ; 43 fiches présentes/non vides.
Recherche de motifs connus de secrets par DevOps : aucun motif trouvé, contrôle non exhaustif.
GET actions/runs?head_sha=2648716caeae74c80d76594cd81d47157b08977e : total_count=0. Aucune CI courante certifiée.
Historique DevOps : run 38187757366 au commit 434eeeaef6e1be38e5d08212854372e5ab71f57b failure ; logs 404 BlobNotFound, cause NON TESTÉ.
Workflow actuel PR/manual uniquement ; aucune exécution déclenchée, quotas/facturation NON TESTÉS.
Ticket #3 encore rédigé pour huit agents. Fiche DEVOPS conserve un handoff direct au DSI. Le validateur ne compare pas tous les rattachements croisés de l'arbre ni la qualité sémantique des fiches.
Aucun code thème/core, ZIP ou visuel dans le snapshot du dépôt.

## Références et conflits
Home prioritaire selon AGENTS : A–G, aucun bloc matières, marine/jaune, textes exacts, viewport 1920×1080 CSS et page entière 1920×H.
V4.2 : Brevet 3AC exclusif, identité pétrole/orange, autre logo/copy/grille. Home : 1AC–3AC. Aucun arbitrage produit inventé.
Les Gates de AGENT_OPERATING_MODEL et de V4.2 portent des critères différents ; toujours nommer document et critères, jamais le numéro seul.
Maquette et logo absents du dépôt. Recherche de fichiers personnels : plusieurs candidats Home Desktop XL/Large et un logo trouvés par leurs métadonnées ; ni inspection de pixels, ni statut d'approbation confirmé. Ne pas déclarer que l'original est perdu ou que ces candidats sont la référence approuvée.
DESIGN_TOKENS.json absent. Codes couleur Home non chiffrés dans le master Home ; ne pas reprendre arbitrairement les tokens V4.2.

## Backlog et dépendances P0/P1
| ID | Priorité | Propriétaire | Acceptation et dépendances | Statut |
|---|---|---|---|---|
| P0-WEB-01 | P0 | SM_ENGINEERING/M_ENGINEERING/TL_WEB_PLATFORM/WP_ARCHITECT | Sources V4 et template Darija accessibles en lecture seule ; dépend de l'accès/export | BLOQUÉ |
| P0-OPS-02 | P0 | SM_TRUST/M_DELIVERY/TL_DEVOPS_RELEASE/DEVOPS | Point de sauvegarde identifié, copie vérifiable et protocole de restauration ; restauration uniquement après accord | NON TESTÉ |
| P0-DES-03 | P0 | SM_PRODUCT/M_PRODUCT/TL_DESIGN_CONTENT/DESIGN_CONTENT | Identifier original approuvé parmi fichiers disponibles, provenance/droits et inspection pixels | NON TESTÉ |
| P0-DSI-04 | P0 | DSI avec SM_PRODUCT | Décision explicite 3AC vs 1AC–3AC et documentation des Gates | BLOQUÉ |
| P0-OPS-05 | P0 | TL_DEVOPS_RELEASE/DEVOPS | CI au commit ciblé, logs et quota vérifiés sans dépense | NON TESTÉ |
| P1-GOV-01 | P1 | SM_TRUST/M_DELIVERY | Actualiser ticket #3 et handoffs ; améliorer validateur après lot approuvé | NON TESTÉ |
| P1-HOME-02 | P1 | SM_PRODUCT + SM_ENGINEERING | Après P0 : Home fidèle, tests clavier/contraste/responsive/FR-AR RTL documentés ; aucune WordPress écriture sans validation | BLOQUÉ |

## Fin de cycle DSI
Statut global audit : BLOQUÉ pour clôture, inventaire partiel vérifié.
Changements réels : documentation d'audit et mise à jour STATUS uniquement dans GitHub ; zéro modification WordPress, zéro installation/activation, zéro publication/DNS, zéro API IA payante.
Tests fonctionnels, performance, sécurité des foyers, RTL et installation ZIP : NON TESTÉ.
Prochaine action : rendre les sources du thème et le rendu authentifié accessibles en lecture seule, identifier le visuel approuvé, puis compléter écarts et rollback avant développement.
