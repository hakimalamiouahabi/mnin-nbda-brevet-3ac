# MNIN NBDA — Organisation CIBLE à 700 profils (proposition)

**Statut : structure définie, NON activée.** Cette proposition est sur la branche `proposal/organization-700` ; elle ne remplace pas l'organigramme opérationnel existant à 43 profils et ne modifie pas WordPress.

## Répartition vérifiée

| Niveau | Nombre |
|---|---:|
| DSI de domaine | 5 |
| Senior Managers | 30 |
| Managers | 60 |
| Team Leaders | 60 |
| Experts catalogués | 545 |
| **Total** | **700** |

Les 5 DSI dépendent d'**un propriétaire unique** qui tranche les priorités. Chaque DSI coordonne 6 Senior Managers, 12 Managers, 12 Team Leaders et 109 experts, soit 140 profils par division. Chaque Senior Manager dispose de 2 Managers ; chacun encadre 1 Team Leader, qui coordonne 9 ou 10 profils experts. Cette hiérarchie suit la répartition demandée, mais peut être trop administrative : éviter les transferts redondants.

## 30 pôles de compétences (545 experts)

| Division | Pôle | Experts | Compétences représentatives |
|---|---|---:|---|
| Design, marque et expérience | Direction artistique, marque et design premium | 19 | Directeur artistique web, Brand designer, Designer typographique, Expert design tokens |
| Design, marque et expérience | Recherche UX et tests utilisateurs | 18 | UX researcher, Expert entretiens utilisateurs, Expert tests utilisateurs, Expert parcours clients |
| Design, marque et expérience | Accessibilité et design inclusif | 18 | Expert WCAG, Designer inclusif, Expert lecteur d’écran, Expert navigation clavier |
| Design, marque et expérience | Illustration 2D et assets vectoriels | 18 | Illustrateur jeunesse, Artiste vectoriel SVG, Expert détourage, Expert dessin de personnages |
| Design, marque et expérience | 3D, animation et expérience WebGL | 18 | Character artist 3D, Rigger, Animateur facial, Animateur procédural |
| Design, marque et expérience | Interface responsive et localisation visuelle | 18 | Designer responsive, Expert tablette, Expert smartphone, Motion designer UI |
| Architecture WordPress et logiciel | Architecture WordPress et ingénierie PHP | 19 | Architecte WordPress, Expert thème, Expert plugin, Architecte PHP |
| Architecture WordPress et logiciel | Backend et API métier | 18 | Ingénieur REST API, Développeur PHP, Ingénieur base de données, Expert permissions |
| Architecture WordPress et logiciel | Frontend HTML, CSS et JavaScript | 18 | Ingénieur frontend, Expert HTML sémantique, Expert CSS moderne, Expert TypeScript |
| Architecture WordPress et logiciel | Gestion des contenus et outils éditoriaux | 18 | Architecte CMS, Expert modèles de contenu, Expert back-office, Expert workflow éditorial |
| Architecture WordPress et logiciel | Performance Web et optimisation | 18 | Expert Core Web Vitals, Expert LCP, Expert INP, Expert CLS |
| Architecture WordPress et logiciel | QA logiciel, CI et déploiement | 18 | Ingénieur CI, QA automation, Expert Playwright, Testeur PHP |
| Pédagogie et programmes scolaires | Référentiels officiels et programmes marocains | 19 | Expert programmes 1AC, Expert programmes 2AC, Expert programmes 3AC, Expert référentiels |
| Pédagogie et programmes scolaires | Ingénierie pédagogique et didactique | 18 | Ingénieur pédagogique, Expert prérequis, Expert diagnostic, Expert feedback |
| Pédagogie et programmes scolaires | Mathématiques et raisonnement | 18 | Enseignant mathématiques, Expert algèbre, Expert géométrie, Expert statistiques |
| Pédagogie et programmes scolaires | Langues arabe, français et anglais | 18 | Expert langue arabe, Expert français collège, Expert anglais collège, Expert expression écrite |
| Pédagogie et programmes scolaires | Sciences expérimentales et technologie | 18 | Expert physique, Expert chimie, Expert SVT, Expert technologie |
| Pédagogie et programmes scolaires | Histoire, géographie, civisme et autres disciplines | 18 | Expert histoire, Expert géographie, Expert éducation civique, Expert éducation islamique |
| Data, analytique et IA maîtrisée | Data engineering et ingestion responsable | 19 | Data engineer, Expert ETL, Expert qualité d'ingestion, Expert données scolaires |
| Data, analytique et IA maîtrisée | Architecture des données et gouvernance | 18 | Data architect, Expert modélisation, Data steward, Expert métadonnées |
| Data, analytique et IA maîtrisée | Data analytics et tableaux de bord | 18 | Data analyst, Expert BI, Expert tableaux élèves, Expert indicateurs |
| Data, analytique et IA maîtrisée | Data science et évaluation de l'apprentissage | 18 | Data scientist, Statisticien, Expert psychométrie, Expert validité mesure |
| Data, analytique et IA maîtrisée | AI engineering local et modèles accessibles | 18 | AI engineer, Expert IA locale, Expert modèles ouverts, Expert inférence |
| Data, analytique et IA maîtrisée | Personnalisation explicable et moteur de règles | 18 | Expert learning analytics, Expert règles adaptatives, Expert connaissances préalables, Expert recommandation |
| Sécurité, opérations et développement produit | Cybersécurité applicative et contrôle d'accès | 19 | Expert AppSec, Expert IAM, Expert threat modeling, Expert pentest autorisé |
| Sécurité, opérations et développement produit | Données des mineurs, vie privée et conformité | 18 | Expert loi marocaine 09-08, Expert protection des mineurs, Expert consentement, Expert CNDP |
| Sécurité, opérations et développement produit | Direction produit, PMO et exécution | 18 | Product owner, Product manager, Scrum master, Expert backlog |
| Sécurité, opérations et développement produit | SEO, recherche et croissance responsable | 18 | Expert SEO technique, Expert contenu organique, Expert métadonnées, Expert search UX |
| Sécurité, opérations et développement produit | Accompagnement élèves, parents et communauté | 18 | Expert support parents, Expert support élèves, Expert aide contextuelle, Expert FAQ |
| Sécurité, opérations et développement produit | FinOps, observabilité et continuité | 18 | Expert FinOps, Expert exploitation, Expert monitoring, Expert alerting |

Chaque pôle dispose de deux équipes, et de 18 à 19 postes d'experts. Les 700 identifiants, niveaux hiérarchiques et rattachements figurent dans `agents/manifest-700-target.json`. Les 545 entrées spécialisées représentent des **postes de rôle**, pas 545 instances d'IA, modèles chargés, collaborateurs recrutés ou prompts individuels déjà qualifiés.

## Gains de temps : mesure, pas affirmation

Plus d'agents peuvent accélérer les **travaux indépendants** (inventaire d'assets, contrôles qualité, tests multi-viewport, documentation). Ils peuvent aussi **ralentir** les tâches fortement couplées (refonte du Hero, validation graphique, intégration WordPress) à cause des conflits, de la revue et de la synchronisation. Il n'existe aucun gain linéaire 43→700. Valider une petite équipe efficace, puis mesurer le débit et la qualité avant d'augmenter la concurrence.

### Activation opérationnelle incrémentale proposée

1. **Pilote Home** : 1 DSI coordinateur et 6 à 12 spécialistes pertinents, sous-agents réellement disponibles seulement.
2. **Traçabilité** : session ou job identifié, commit/PR, tests exécutés, preuve et coût/quota. Ne jamais déclarer 700 agents actifs sur la seule base du manifest.
3. **Montée en charge** : augmenter jusqu'à la capacité effectivement autorisée de Codex / Work, uniquement si les gains sont mesurés et sans nouvelle dépense.
4. **Critères** : temps de cycle par maquette validée, taux d'écarts visuels, poids des assets, qualité responsive, résultats QA, conflits de modifications et temps de revue humaine.

### Règles non négociables

- Maquette Home officielle V1.0 figée, **pas de régénération destructrice des illustrations**.
- Qualité web : privilégier SVG pour les éléments vectoriels, originaux HD pour les images raster et exports adaptés aux densités d'affichage. Un fichier agrandi « 8K » n'est pas automatiquement plus net.
- Aucune publication WordPress ni déploiement ou installation sans validation explicite.
- Aucune API IA payante, aucun wallet, abonnement ou frais additionnels.
- Protection des données des mineurs, sources officielles vérifiées, décisions documentées.
- Tous les lots ont un statut `PASS`, `FAIL`, `NON TESTÉ`, ou `BLOQUÉ` avec preuve.

## Décision d'architecture

L'organisation à 700 est un **catalogue cible** : pour la rendre exécutable, il faudrait qualifier les prompts, choisir un ordonnanceur réel, définir des sessions et des limites de parallélisme, connecter GitHub à l'environnement d'exécution, enregistrer des preuves et vérifier les quotas. Aucune de ces étapes n'est implicitement réalisée par un commit.
