# Matrice QA responsive — Home MNIN NBDA
Date : 12 octobre 2026. Référence : [ticket #5](https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/issues/5).

**Tous les statuts ci-dessous sont volontairement « NON TESTÉ ».** Le dépôt distant ne contient pas encore le prototype HTML/CSS de la session Codex initiale. Les résultats de la transcription Codex ne prouvent pas de nouveaux tests exécutés depuis cette reprise.

## Captures obligatoires (19 cas, 38 captures minimales)
Pour chaque taille : une capture du viewport visible + une capture pleine page, avec indication du navigateur, zoom/DPR et commit. Captures réelles, non redimensionnements de l'image PNG aplatie.

| Famille | Viewport CSS (L × H) | Capture visible | Capture page entière | Reflow / overflow |
|---|---|---|---|---|
| 4K | 3840 × 2160 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Desktop XL | 1920 × 1080 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Desktop Large | 1600 × 900 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Laptop Large | 1440 × 900 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Laptop Standard | 1366 × 768 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Laptop Compact | 1280 × 800 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Tablette XL | 1024 × 1366 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Tablette 11 pouces | 834 × 1194 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Tablette 10–11 pouces | 820 × 1180 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Tablette 10 pouces | 768 × 1024 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Petite tablette | 600 × 960 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Mobile XL | 430 × 932 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Mobile Large | 412 × 915 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Mobile Medium | 390 × 844 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Mobile Standard | 375 × 812 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Mobile Compact | 360 × 800 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Petit mobile | 320 × 568 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Paysage tablette | 1180 × 820 | NON TESTÉ | NON TESTÉ | NON TESTÉ |
| Paysage mobile | 932 × 430 | NON TESTÉ | NON TESTÉ | NON TESTÉ |

## Scénarios d'acceptation (tous NON TESTÉ depuis cette reprise)
| Contrôle | Critère | Statut |
| --- | --- | --- |
| HTML responsive réel | Texte en DOM, sections sémantiques, un seul H1, pas de PNG plein écran | NON TESTÉ |
| Grille | Aucun débordement horizontal non intentionnel à 320 px et autres formats | NON TESTÉ |
| Header | Logo identique, menu navigable sur petits écrans et au clavier | NON TESTÉ |
| Hero | Même texte et même Amine, zone stable, ordre de lecture logique | NON TESTÉ |
| Carte Mission | Pictogrammes lisibles, aucun masquage de texte | NON TESTÉ |
| Bénéfices | Quatre éléments réorganisés sans perte de sens | NON TESTÉ |
| Parcours | Trois cartes 1AC / 2AC / 3AC, sans modification de leurs illustrations | NON TESTÉ |
| CTA | Boutons accessibles avec JS désactivé, destination vérifiée | NON TESTÉ |
| Cibles tactiles | Recontrôler et corriger les 9 cibles inférieures à 44 px signalées par Codex | NON TESTÉ |
| Clavier | Focus visible, ordre logique, pas de piège clavier | NON TESTÉ |
| Localisation | Vérification français/arabe RTL sans inversion accidentelle de contenus | NON TESTÉ |
| Zoom | Lisibilité et navigation à 200 % | NON TESTÉ |
| Mouvement réduit | `prefers-reduced-motion: reduce` neutralise les animations inutiles | NON TESTÉ |
| Faible capacité | Contenu essentiel avec JS/WebGL désactivés, `saveData` pris en compte | NON TESTÉ |
| WebGL | Pas de GLB non approuvé ; poster 2D conservé, fallback testé | NON TESTÉ |
| Navigateurs | Chrome, Firefox, Safari, Android/iOS réels | NON TESTÉ |
| Performance | LCP / INP / CLS sur contexte mesuré, protocole et matériel consignés | NON TESTÉ |
| Confidentialité | Aucune donnée comportementale sur les mineurs transmise | NON TESTÉ |
| WordPress | Aucune écriture en production ou staging | PASS — aucun outil WordPress utilisé durant cette reprise GitHub |

## Comparaison artistique
Le respect exact de la Home approuvée nécessite le PNG source, ses assets originaux et des captures du HTML dans les tailles ci-dessus. Aucun résultat de « pixel perfect » ne peut être reconduit sur la seule foi d'une transcription.

**Décision actuelle : P1 responsive = BLOQUÉ en attente de la récupération du code source ; validation visuelle et tests multi-appareils = NON TESTÉ.**
