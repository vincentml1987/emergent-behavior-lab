# Run 3 — status: no confirmed oscillation (yet)

Initially suspected a repeat at Breed 3 (matched Breed 0 on the three
fresh-rebirth values and which trio was alive), but that match didn't hold
up under scrutiny:

- Breed 4 did not match Breed 1.
- Breed 5 did not match Breed 0 or Breed 2.
- Breed 6 did not match Breed 3.
- Through Breed 7, no two breed states have repeated.

Conclusion: the Breed 0 / Breed 3 similarity was two states that looked
alike (same alive/dormant trio shape, close rebirth values), not a true
cycle. **Flagging this run as no confirmed oscillation through Breed 7.**

## Open thread worth following up

One real pattern did hold across all 7 recorded breeds: a newborn with
population exactly **71** has appeared in every single one (F in breeds 0,
1, 3, 6, 7; D in breed 4; C in breed 5). The letter it lands on moves
around, but something about the underlying bred content doesn't. Possible
next step: read the live creation log (records each child's exact parent
pair) to check whether these all trace back to the same two original
patterns recombining, rather than inferring it from population numbers
alone.

## Update: convergence, not oscillation

Much later in this same run (gen ~3081-3230, see
`convergence-gen3081-3230.png`), four of the six currently-alive universes
(A, B, E, F) show **identical** population legends - not similar, exact:
`0,0:18`, `-1,1 (gone):14`, `0,1 (gone):4`, `0,-1 (gone):4`, and two more at
0 - same values, same curve shape, across all four.

This reframes the whole investigation. We were hunting for a repeating
*sequence* of distinct states (a cycle). What seems to actually be
happening is a shrinking pool of distinct original patterns in
circulation - repeated XOR-breeding collapsing diversity, the way genetic
drift can collapse a population toward one genotype - except here it's
landing in multiple slots (4 of 6) at once rather than driving the rest
extinct. That would explain why no short letter-level cycle was ever found:
wrong thing to look for. Next step to confirm: read the live creation log
for these universes' lineages and verify whether their original tiles are
literally the same bred pattern reappearing, or merely converging toward
very similar-looking but distinct ones.

## Update: total extinction followed the convergence

Very next recorded window (gen 3111-3260, see
`total-extinction-gen3111-3260.png`): all six universes at `0,0:0`. The
four-way identical convergence (A/B/E/F) seems to have led directly to a
correlated death - if those four really shared content, they'd share a
fate too - and C/D apparently followed close behind, wiping the whole
lineup at once.

This is a real test of the simultaneous-death backfill rule (added after
the first "more complex oscillation" investigation): with zero survivors,
the normal "3 alive -> breed" trigger has nothing to breed from, so
recovery depends on pulling the longest-lived of whichever universes died
in that same tick back in by their frozen original pattern. Worth
confirming directly whether the run actually self-recovered via that path
or needed manual intervention.

## Files

- `breed-00.png` through `breed-07.png` (breed-02 missing - not captured)
- `convergence-gen3081-3230.png` - four-way identical-population snapshot,
  much later in the same run
