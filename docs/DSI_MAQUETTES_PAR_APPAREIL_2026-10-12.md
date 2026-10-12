# DSI — Maquettes Home par dimension et type d'appareil
Date : 12 octobre 2026. Dossier : #5. Branche de revue : `audit-reprise-home-2026-10-12`.

## Exécution réelle
Coordination DSI exercée dans une conversation ChatGPT. Les 43 rôles restent des définitions documentées ; **aucun sous-agent Codex autonome n'a été lancé pour ce lot**.

## Source graphique
La Home approuvée, à conserver intégralement, correspond au PNG `MNIN_NBDA_HOME_REFERENCE_V1_0.png`, 1024 × 1536, SHA-256 `393dfd6498180398023b712ef9d68e95a902ac6e0d5b5845818bc75c3b53166e` — **PASS, empreinte revérifiée**.

## Archive retrouvée
Le fichier `MNIN_NBDA_PACK_WORDPRESS_RESPONSIVE_21_FORMATS.zip`, retrouvé dans la bibliothèque de fichiers de la conversation, contient :
- Le PNG officiel exact et ses ressources reprises dans un prototype HTML/CSS ;
- 21 PNG correspondant à la fenêtre visible, et 21 captures PNG pleine page ;
- Un `index.html` avec structure et points de rupture CSS ;
- Un rapport de dimensions et des assets.

**Important :** ces 42 images sont des captures **préexistantes**, non des captures recalculées dans cette reprise. Elles ont été contrôlées et regroupées. La navigation Chromium a été refusée dans l'environnement de reprise (`ERR_BLOCKED_BY_ADMINISTRATOR`) ; ne pas attribuer à cette session une exécution de tests navigateur non réalisée.

## Inventaire exact des 21 tailles (pixels CSS)
| Famille | Formats couverts |
| --- | --- |
| Ordinateurs (8) | 3840×2160, 1920×1080, 1600×900, 1536×864, 1440×900, 1366×768, 1280×800, 1280×720 |
| Tablettes (6) | 1032×1376, 1024×1366, 834×1194, 820×1180, 768×1024, 600×960 |
| Mobiles (7) | 430×932, 412×915, 393×852, 390×844, 375×812, 360×800, 320×568 |

## Statuts mesurables
- **PASS** : référence officielle (SHA-256 exact) ;
- **PASS** : 42 PNG archivés, toutes les dimensions de fenêtre/pleine page correspondant au manifeste vérifiées directement sur les pixels du fichier ;
- **PASS** : archivage et classement par famille, empreintes individuelles consignées ;
- **NON TESTÉ** : reproduction Chromium de ces 42 images pendant cette session, tests multi-appareils et comparaison « pixel-perfect » avec la référence graphique (le responsive impose un reflow) ;
- **FAIL constaté dans le HTML archivé** : l'instruction CSS mobile masquant le saut de ligne fusionne visuellement « corrigés » et « et » ; correction nécessaire avant validation finale ;
- **NON TESTÉ** : accessibilité, contraste, claviers, AR/RTL, iOS, Safari, Firefox, Web Vitals ;
- **NON PRODUITS** : deux formats paysage prévus par #5 (1180×820 et 932×430), car absents des captures source ;
- **BLOQUÉ** : destination WordPress réelle des liens provisoires du prototype ; ne pas publier tel quel ;
- **BLOQUÉ** : validation artistique 3D d'Amine ; conserver le poster canonique, ne pas intégrer le GLB non conforme.

## Livrables et arbitrage
Les trois archives par famille et l'archive intégrale sont remises dans la conversation, **pas versées dans ce dépôt**. Les fichiers HTML et images doivent faire l'objet d'une revue visuelle avant intégration. Cette entrée GitHub est uniquement documentaire et ne doit pas être interprétée comme validation ou livraison du prototype Codex historique.

Aucune publication WordPress/staging, aucun DNS, aucune fusion dans `main`, aucune API payante.

**Décision DSI : 21 déclinaisons disponibles pour validation humaine ; interdiction de présenter ce lot comme prêt pour production.**
