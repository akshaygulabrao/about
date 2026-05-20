---
title: "Chessckers, Part 1: The Game"
date: 2026-05-17
draft: false
tags: ["chess", "checkers", "games", "ai", "alphazero"]
math: true
---

## 1. Why this series

I designed a two-player game called **Chessckers**. White plays standard FIDE chess. Black plays a checkers-derived swarm: stones and kings stacked into towers that slide and hop diagonally, with a separate orthogonal "charge" reserved for kings. The two sides share a board but almost nothing else — different pieces, different movement, different win conditions.

This series is about trying to train an [AlphaZero-style](https://arxiv.org/abs/1712.01815) engine to play it superhumanly. The asymmetry is the whole point. Standard AlphaZero domains (chess, shogi, Go) are zero-sum, perfect-information, and symmetric — both players draw from the same action space. Chessckers breaks the symmetry, and I want to know whether a single network with shared weights can still learn both sides simultaneously.

Before any of that: the rules. This post is the first part — what the game is and how it plays. Subsequent parts will cover board representation, the action space, MCTS, network architecture, and training.

## 2. Board and setup

The board is the standard 8×8 grid. Around it sits a **rim** — the 10×10 perimeter one square outside the board on every side. White pieces never touch the rim. Black towers may step onto it mid-capture, but no Black turn can ever end on a rim square.

Files and ranks are 1–8 as in chess, with White starting on ranks 1–2 and Black on ranks 6–8.

**White.** Standard FIDE setup. Pawns on rank 2, the back row on rank 1.

**Black.** 24 single-piece towers, one per square on ranks 6–8: **stones** on ranks 6 and 8, **kings** on rank 7.

<figure style="max-width:420px;margin:1.5em auto">
  <img src="../../images/chessckers/initial-position.svg" alt="Initial position. White (standard FIDE setup) on ranks 1–2; Black stones on ranks 6 and 8, kings on rank 7. The dashed perimeter is the rim." style="width:100%">
  <figcaption style="font-size:0.85em;text-align:center;margin-top:0.4em;color:#666">Initial position. White on ranks 1–2; Black stones on ranks 6 &amp; 8, kings on rank 7. Dashed perimeter is the rim.</figcaption>
</figure>

A **tower** is an ordered stack of Black pieces sharing one square. Its **height** \(n\) is the number of pieces. The **top piece** governs the tower's capabilities, and the height \(n\) is both the maximum distance the tower can travel on a non-capturing move and the maximum distance it can scan along a diagonal when looking for capture targets. Every action below either preserves or rearranges towers — Black pieces never exist off-tower.

Distance on the board is Chebyshev: \(\operatorname{dist}(p_1, p_2) = \max(|x_1 - x_2|, |y_1 - y_2|)\). Diagonals and orthogonals both count one square per step.

## 3. White's moves

White plays standard FIDE chess — same legal moves, same check rules, same castling, same en passant, same pawn promotion. The only modification is the capture effect: **when a White piece captures a Black tower, the entire tower is removed**, regardless of height or composition. There is no partial capture, no skimming the top piece. A pawn that takes a king-topped tower of height 5 wipes all five pieces from the board.

White also never enters the rim. The rim exists for Black's mechanics only.

## 4. Black's moves

Black has three families of action, separated cleanly by purpose.

### 4A. Quiet moves (no capture)

Three options, each ends the turn. A quiet move can land on an empty square or a friendly tower; landing on a friendly tower **merges** the moving piece(s) onto its top, producing a taller tower. A quiet move never lands on White.

1. **Diagonal slide.** The whole tower moves up to \(n\) squares along one diagonal. If the top piece is a stone, only forward diagonals (toward rank 1) are legal; if the top piece is a king, any diagonal works.

   <div style="display:grid;grid-template-columns:1fr 1fr;gap:1em;margin:1.5em auto;max-width:560px">
     <figure style="margin:0">
       <img src="../../images/chessckers/stone-e6.svg" alt="Height-1 stone on e6 with arrows to d5 and f5" style="width:100%">
       <figcaption style="font-size:0.85em;text-align:center;margin-top:0.4em;color:#666">Height-1 stone on e6: slides one square forward-diagonal to d5 or f5.</figcaption>
     </figure>
     <figure style="margin:0">
       <img src="../../images/chessckers/king-e6.svg" alt="Height-1 king on e6 with arrows to d5, f5, d7, f7" style="width:100%">
       <figcaption style="font-size:0.85em;text-align:center;margin-top:0.4em;color:#666">Height-1 king on e6: any diagonal — d5, f5, d7, f7.</figcaption>
     </figure>
     <figure style="margin:0">
       <img src="../../images/chessckers/stone-king-e6.svg" alt="[stone, king] stack on e6 with arrows to d5, f5, d7, f7 (near) and c4, g4, c8, g8 (far, curved)" style="width:100%">
       <figcaption style="font-size:0.85em;text-align:center;margin-top:0.4em;color:#666">[stone, king] stack on e6 (king on top): up to 2 squares along any diagonal — near (d5/f5/d7/f7) and far (c4/g4/c8/g8).</figcaption>
     </figure>
     <figure style="margin:0">
       <img src="../../images/chessckers/stone-stone-e6.svg" alt="[stone, stone] stack on e6 with forward-diagonal arrows to d5, f5 (near) and c4, g4 (far, curved)" style="width:100%">
       <figcaption style="font-size:0.85em;text-align:center;margin-top:0.4em;color:#666">[stone, stone] stack on e6 (stone on top): forward diagonals only, up to 2 squares — d5/f5 (near) and c4/g4 (far).</figcaption>
     </figure>
   </div>

2. **Deploy.** Take the top \(s\) pieces off a tower (\(1 \le s < n\)) and move them as a smaller sub-tower up to \(s\) squares along a diagonal. The remaining \(n - s\) pieces stay put. The sub-tower's top is the same piece that was on top of the original, so the Stone-vs-King direction rule still applies. Deploys are the main mechanism by which Black distributes force across the board.

   <figure style="max-width:680px;margin:1em auto">
     <div style="display:flex;align-items:center;justify-content:center;gap:0.5em">
       <img src="../../images/chessckers/deploy-e5-c3.svg" alt="Before: [s, s, s, K] stack on e5 with arrow showing deploy of 2 pieces to c3" style="flex:1;min-width:0;max-width:300px">
       <span aria-hidden="true" style="font-size:2em;color:#666;line-height:1;flex:0 0 auto">→</span>
       <img src="../../images/chessckers/deploy-e5-c3-after.svg" alt="After: [s, s] on e5 and [s, k] on c3" style="flex:1;min-width:0;max-width:300px">
     </div>
     <figcaption style="font-size:0.85em;text-align:center;margin-top:0.4em;color:#666">Deploy <code>e5c3[2]</code>: top 2 pieces [s, k] move 2 squares SW from e5 to c3; [s, s] remain on e5.</figcaption>
   </figure>

3. **Back rank sprint.** A height-1 stone tower on rank 8 that has never moved may sprint two squares forward-diagonal. The path must be clear. This is structurally analogous to a chess pawn's double move — a one-time speed boost off the starting square. Each stone carries a private `hasMoved` flag that persists when its tower merges into a larger one, so a stone gets exactly one sprint in its lifetime.

   <figure style="max-width:420px;margin:1.5em auto">
     <img src="../../images/chessckers/back-rank-sprint.svg" alt="Unmoved height-1 stone on e8 sprinting two squares forward-diagonal to c6 or g6" style="width:100%">
     <figcaption style="font-size:0.85em;text-align:center;margin-top:0.4em;color:#666">Back rank sprint: unmoved stone on e8 jumps two squares forward-diagonal to c6 or g6.</figcaption>
   </figure>

### 4B. Diagonal captures: hops and chains

This is the heart of Black's offense.

A **hop** walks along one diagonal, captures every White piece it passes over, and lands somewhere on the same diagonal. A turn can be a single hop or a **chain** — several hops in different directions, glued together by a shared cadence.

**Single hop.** Pick a diagonal. The tower scans up to \(n\) squares looking for a **first enemy** — the first White piece on the diagonal. (Stone-topped towers only scan forward; king-topped towers scan any direction.) Friendly towers block the scan. If no White piece appears within \(n\) steps, no hop is available in that direction.

Once the first enemy is located at distance \(d\), the player picks a **landing distance** \(k \in [d{+}1,\, n{+}1]\). The tower walks \(k\) steps from its start square. Every White piece on the path at steps \(1, \ldots, k{-}1\) is captured. The first enemy is always among them, because \(k > d\). What happens at step \(k\) depends on what's there:

- **Empty board square.** Normal landing. The tower survives.
- **Friendly tower.** Illegal at that \(k\). Try a different \(k\) in the same direction.
- **White piece (a "ram").** The moving tower is *destroyed* at the landing square. The landing White is *not* captured — only the path Whites are. Ramming requires \(k > d\), which is already enforced by the choice of \(k\).
- **Rim square.** The hop lands on the rim. Mid-chain, the next hop continues from the rim. At end of turn, see the fallback rule below.

Note that landing on the first enemy itself (\(k = d\)) is not a legal hop — there's nothing to hop *over*. And the slot at distance \(n{+}1\) is reserved for landings only: a White piece reached only at step \(n{+}1\) is not a first enemy, so a tower can't initiate a capture against it.

**Chain.** After a non-ram hop, the tower may continue with another hop in any direction *except* the 180° reverse of the one just played (no immediate backtracking). The chain has a **cadence** equal to the \(k\) used by the first hop, and every continuation hop must walk *exactly* cadence steps. So the first hop gets free choice of distance; the rest are locked. If a candidate direction has no first enemy within cadence steps, or its trace would step off the 10×10 grid before reaching cadence, that direction is unavailable.

The player can stop the chain after any capture — continuation is always optional. A ram or running out of legal directions ends the chain.

**End-of-turn fallback.** Black must end the turn on the board. If the final hop lands on a rim square, the tower retreats to the last on-board square its path visited before stepping onto the rim. Mid-chain rim landings are fine, but you can't *stop* there.

**Promotion mid-chain.** If any hop's path touches rank 1 — by landing there or by stepping through it on the way to a rim square — every stone in the tower promotes to a king *before* the next hop is considered. A stone-topped tower mid-chain can become king-topped, and the rest of the chain immediately gains access to backward diagonals. Promotion happens during the chain, not just at the end.

### 4C. Charge: the king-tower orthogonal

A king-topped tower may move along a rank or file in a single straight line. The path squares must contain no friendly towers (rim squares are allowed mid-path). Every White on the path's intermediate squares is captured for free — captures cost nothing.

The cost is paid in kings. **One king is demoted to a stone per square moved.** If the tower has more kings than the cost requires, the player picks which ones to demote (kings are 1-indexed from the bottom). Demoted kings become stones with `hasMoved = true`, so they can't sprint afterwards. The post-demotion top piece governs the tower's mobility on its next turn — the demotion choice is strategic.

Landings work like diagonals: empty (land there), friendly (merge), White (ram — moving tower destroyed, landing White not captured), or rim (fallback to last on-board square). Charging rams require at least one path capture first, so a distance-1 charge can never ram.

A charge ends the turn — no chaining onto a charge, no chaining off one. **Charges never promote**: landing on rank 1 via a charge does nothing to the tower's stones. Only diagonal moves promote.

## 5. The mandatory rule

At the start of Black's turn, every Black tower is scanned along its legal diagonals (forward only for stone-top, any for king-top) for **adjacent Whites that admit a normal-landing diagonal hop** — meaning a hop that lands on an empty board square. If at least one such hop exists anywhere on the board, the **mandate** is active for that turn.

While the mandate is active, only capturing moves are legal — diagonal hops (normal or ram), capturing charges, or charging rams. Quiet diagonals, deploys, sprints, and non-capturing charges are suppressed for the turn. Black cannot pass on a free piece.

Three subtleties worth flagging, because they're easy to get wrong:

- **Rams count, but are never forced.** The trigger looks only at normal-landing hops, so a position whose only capture options are rams (or rim-only landings) doesn't fire the mandate at all. Once the mandate *is* active, a ram is a valid way to fulfill it — but the player will always have at least one non-ram option to choose instead.
- **Only the first capture is forced.** Chain continuation is always optional. The mandate forces you to start capturing; it doesn't force you to keep chaining.
- **The trigger is recomputed every turn.** Fulfilling the mandate on turn \(t\) does not silence whatever new threats appear at the start of turn \(t{+}1\).

## 6. Promotion and win conditions

**Promotion.** Any non-charge Black move (quiet diagonal, deploy, sprint, hop, hop chain) whose path touches rank 1 promotes every stone in the moving tower to a king. Promotion takes effect immediately, including mid-chain. Charges never promote.

**White wins** if Black has no pieces on the board, *or* if Black has no legal moves on their turn. Chessckers does not treat a Black stalemate as a draw — being unable to move loses the game.

**Black wins** by checkmating the White king under standard FIDE rules.

## 7. What makes this hard for an engine

That's the game. To set up the rest of the series, here is what I expect to be hard about training an AlphaZero-style engine for it:

- **Asymmetric action spaces.** AlphaZero's chess action encoding has 4672 plane-channels of moves per square. White in Chessckers needs roughly the same. Black needs something else entirely — towers, deploys parameterized by \(s\), chains with variable-length continuations. The two sides do not share an action representation.
- **Variable-length actions.** A capture chain is not a single primitive. It's a sequence of decisions with branch points, each with its own legality conditions (cadence, no 180° reverse, no off-grid step, mid-chain promotion). How to expose this to MCTS — as a flat enumeration of full chains, as a sequence of per-hop decisions, or as some hybrid — is a real design choice.
- **Stacked state.** Each board square can host a tower of arbitrary height with arbitrary stone-vs-king composition and per-stone `hasMoved` flags. The board tensor is not a simple per-square one-hot. Truncation strategies (max tower height?) bake assumptions into the network.
- **Globally conditional legality.** The mandatory rule means whether a given quiet move is legal depends on whether *some other* tower can capture. Standard chess legality is local to the moving piece; Chessckers legality is not.
- **No stalemate draw.** Eliminates one of the major draw modes AlphaZero had to learn to navigate in chess, but introduces a sharp evaluation cliff near zugzwang positions.

Part 2 will be the board and action-space representation — how this gets serialized into tensors a network can actually consume.
