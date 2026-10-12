# MNIN NBDA — Exécution DSI : déclinaisons fidèles à la Home officielle
Date : 12 octobre 2026. Ticket : #5. Sans WordPress ni déploiement.

## Référence figée (PASS)
Fichier transmis par le propriétaire : `Ta mission _ un déclic aujourd’hui.png`.
PNG RGBA 1024 × 1536 ; SHA-256 **`393dfd6498180398023b712ef9d68e95a902ac6e0d5b5845818bc75c3b53166e`**, vérifié sur le binaire de cette conversation.
Le visuel conservé dans l'archive de livraison a le même SHA-256. Priorité absolue à **cette maquette**, plutôt qu'aux archives graphiques plus anciennes.

## Travaux réellement exécutés par spécialité
Ces fonctions correspondent aux rôles documentés dans `agents/manifest.json`, coordonnés **séquentiellement par un seul assistant dans ce chat**. Aucune instance Codex autonome ni sous-agent distinct n'a été lancée.

| Responsabilité | Exécution | Statut |
| --- | --- | --- |
| DSI / TL_DESIGN_CONTENT | Contrôler PNG et préserver logo, Amine, textes, carte Mission, 1AC-2AC-3AC, bandeau final | PASS contrôle source ; validation esthétique NON TESTÉ |
| TL_WEB_PLATFORM / RESPONSIVE_MOBILE | Partir du HTML/CSS du prototype retrouvé en bibliothèque, corriger les cibles tactiles et la jonction « corrigés et », rendre 23 tailles CSS | PASS captures Chromium |
| TL_QA_SECURITY | Tester débordement horizontal, H1, chargement d'images, dimensions, menu mobile JS activé/désactivé | 23/23 PASS **sur ces contrôles techniques uniquement** |
| TL_DEVOPS_RELEASE | Archiver séparément la référence intacte, le prototype de travail, les images et le manifeste de 46 nouvelles captures | PASS ZIP local et contrôle d'intégrité |

## Captures **nouvelles** depuis ce chat
Rendu réel d'un DOM HTML/CSS via Chromium headless Playwright (le navigateur bloquant la navigation `file://`, assets locaux temporairement intégrés comme data URI dans `page.set_content` pour les seules captures). DPR 1 et `prefers-reduced-motion: reduce`. 23 formats, **46 PNG** (viewport + pleine page).

- **Ordinateurs (8)** : 3840×2160 ; 1920×1080 ; 1600×900 ; 1536×864 ; 1440×900 ; 1366×768 ; 1280×800 ; 1280×720.
- **Tablettes (6)** : 1032×1376 ; 1024×1366 ; 834×1194 ; 820×1180 ; 768×1024 ; 600×960.
- **Mobiles (7)** : 430×932 ; 412×915 ; 393×852 ; 390×844 ; 375×812 ; 360×800 ; 320×568.
- **Paysage (2)** : 1180×820 ; 932×430.

Tous les cas : bonne résolution PNG, page complète, **pas de débordement horizontal**, images chargées, H1 unique : **PASS**.
Menu mobile JS et navigation de secours sans JS : **PASS** lors de cette campagne.
Cibles de menu et flèches des cartes au minimum 44×44 px en format mobile : **PASS**.

## Réserves et conformité
- La source visuelle est exacte, mais les captures HTML/CSS ne sont **pas revendiquées pixel-perfect**. Ratio Hero, notes manuscrites et placement des éléments à approuver artistiquement sur chaque famille d'écran.
- Les ressources individuelles du prototype sont des découpes non authentifiées comme masters graphiques originaux.
- Les routes d'inscription/connexion et niveaux sont encore des ancres provisoires ; **BLOQUÉ pour publication**.
- 3D d'Amine non validée : **aucun GLB intégré**.
- RTL arabe, zoom 200 %, VoiceOver/TalkBack, Firefox/Safari, iOS/Android physiques, LCP/CLS/INP réels : **NON TESTÉ**.
- Le code de cette livraison n'est **pas** le commit original local Codex `ef24acc` ; ce dernier reste à récupérer séparément.
- Aucun changement de WordPress, de DNS ou de branche `main`, aucune API IA payante.

## Livrables
Les archives ZIP téléchargeables, 4 planches contact, `index.html`, 16 fichiers d'assets, la référence PNG originale intacte, les 46 captures et un manifeste SHA des captures sont fournis dans la conversation ChatGPT du 12 octobre. Aucun binaire nouveau n'est versé sur GitHub par ce commit documentaire.

**Décision : rendu multi-écrans prêt pour revue humaine ; pas de livraison WordPress avant approbation visuelle et fonctionnelle.**
