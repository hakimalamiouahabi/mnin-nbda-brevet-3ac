# MNIN NBDA — Preuve partielle Task 6, transcriptions fournies par le propriétaire

**Date : 12 octobre 2026. Statut : SOURCE PARTIELLE, COMMITS CODEX ORIGINAUX NON RÉCUPÉRÉS.**

Ce document archive le contenu exploitable des deux transcriptions apportées le 12 octobre par le propriétaire.
Ce document n'est **pas** un export du worktree, pas un commit de Codex et pas la preuve que les tests ont été exécutés dans le dépôt GitHub actuel.

## Identification de l'environnement d'origine d'après les transcriptions

- Espace de travail signalé : `/workspace/mnin-nbda-brevet-3ac/.worktrees/chemin-lumineux/`.
- Branche de travail locale signalée : `feature/chemin-lumineux`.
- Référence principale du prototype : `prototype/chemin-lumineux/`.
- Commits locaux rapportés : `7ca83f7` (machine d'état) et `ef24acc` (Hero interactif).
- **GitHub direct** : seuls `main` et `audit-reprise-home-2026-10-12` sont visibles lors de ce contrôle ; `ef24acc` n'est pas résolu sur le distant.
- Le script `controller.js` ci-dessous est recopié du texte communiqué, pas issu d'un `git show ef24acc`.

## Sept fichiers annoncés comme modifiés par la Task 6
1. `prototype/chemin-lumineux/tests/e2e/hero-interaction.spec.js` — source complète non récupérée.
2. `prototype/chemin-lumineux/src/app.js` — source complète non récupérée.
3. `prototype/chemin-lumineux/src/interaction/controller.js` — **61 lignes récupérées du texte**.
4. `prototype/chemin-lumineux/src/styles.css` — source complète non récupérée.
5. `prototype/chemin-lumineux/tests/e2e/static-home.spec.js` — source complète non récupérée.
6. `prototype/chemin-lumineux/tests/visual/home-static.spec.js` — source complète non récupérée.
7. `prototype/chemin-lumineux/reports/gate-c-hero.md` — **51 lignes récupérées du texte**.

## Code exact déclaré pour controller.js dans la transcription

Empreinte du fichier réextrait localement : SHA-256 `d1d0f752bf10c1d29ced390490e57d8b607c6eae514f3a8b8e5adb83ecaf0dcf`.
Vérification locale `node --check` : **PASS**. Aucun test d'intégration ni test E2E réexécuté.

```js
const CTA_GAZE = Object.freeze({ x: -1, y: 0, z: 1 });
const NEUTRAL_GAZE = Object.freeze({ x: 0, y: 0, z: 1 });

/**
 * Connect the primary CTA to the deterministic scene state machine.
 * Pointer and keyboard presence are tracked separately so leaving with the
 * pointer does not cancel a still-focused keyboard interaction.
 */
export function createInteractionController(root, machine, scene) {
  if (!root || !machine?.send || !scene?.play || !scene?.lookAt) {
    throw new TypeError('createInteractionController requires root, machine and scene');
  }

  const cta = root.querySelector('[data-scene-target="cta-primary"]');
  if (!cta) throw new TypeError('The primary CTA scene target is missing');

  const activeInputs = new Set();
  let started = false;

  const enter = input => {
    const wasInactive = activeInputs.size === 0;
    activeInputs.add(input);
    if (!wasInactive) return;
    if (machine.send('CTA_ENTER') !== 'cta') return;
    scene.play('PointCTA');
    scene.lookAt(CTA_GAZE);
  };

  const leave = input => {
    activeInputs.delete(input);
    if (activeInputs.size || machine.state !== 'cta') return;
    if (machine.send('LEAVE') !== 'idle') return;
    scene.play('ReturnIdle');
    scene.lookAt(NEUTRAL_GAZE);
  };

  const onPointerEnter = () => enter('pointer');
  const onPointerLeave = () => leave('pointer');
  const onFocus = () => enter('focus');
  const onBlur = () => leave('focus');

  return Object.freeze({
    start() {
      if (started) return;
      started = true;
      cta.addEventListener('pointerenter', onPointerEnter);
      cta.addEventListener('pointerleave', onPointerLeave);
      cta.addEventListener('focus', onFocus);
      cta.addEventListener('blur', onBlur);
    },
    destroy() {
      if (!started) return;
      started = false;
      activeInputs.clear();
      cta.removeEventListener('pointerenter', onPointerEnter);
      cta.removeEventListener('pointerleave', onPointerLeave);
      cta.removeEventListener('focus', onFocus);
      cta.removeEventListener('blur', onBlur);
    },
  });
}
```

## Résultats Task 6 rapportés, NON REVÉRIFIÉS
- 12/12 E2E Chromium PASS **d'après Codex**.
- 52/52 unitaires PASS **d'après Codex**.
- 2/2 visuels PASS, 0 pixel différent **d'après Codex**.
- Build Vite PASS **d'après Codex**.
- Rapport `gate-c-hero.md` : poster immédiat, canvas déclaré sans CLS, navigation native et fallback WebGL/404/timeout/reduced-motion/saveData.
- Modèle GLB définitif : NON TESTÉ artistiquement.

## Revue indépendante visible dans capture fournie : CHANGES REQUESTED
Le résultat global **ne doit pas être étiqueté PASS** :
1. Canvas transparent superposé au poster complet, pouvant laisser deux Amine visibles pendant l'animation (absence de masquage local).
2. `/assets/amine/amine.glb` demandé par `app.js` mais non suivi par Git au commit `ef24acc` : 404 probable si on ne livre que ce commit.
3. Aucun scénario tactile `pointerdown / pointerup / pointercancel` démontré, malgré les tests survol/focus.
4. Relecture et validation humaine du modèle artistique toujours nécessaires.

## Procédure de récupération du vrai code

Se référer à `docs/CODEX_RECOVERY_RUNBOOK_2026-10-12.md`. Dans la session Codex d'origine,
inventorier `git worktree list --porcelain`, `git log --all --oneline`, `git status`
et les commits sans aucun reset/clean/force push. Sauvegarder les changements non commités avant de pousser les commits
existants sur une nouvelle branche isolée.

**Aucune modification de `main`, WordPress, DNS ou de la maquette officielle par ce document.**
