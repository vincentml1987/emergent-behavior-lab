# Run 4 — confirmed: recurring genotypes + a real local oscillator

First run analyzed via the database pipeline instead of screenshots
(`data/gol-export-gen1488-1791096352578.json`, imported under run label
`oscillation-4`, `run_id=2` in `data/lab.sqlite`). Single export at
gen 1488, but its embedded `creationLog`/`popHistory` cover the universes'
full history back to their birth, so one export was enough to work with.

Params: 48x32 grids, auto-pause off, no grid lifespan, stall window 100
gens / tolerance 0.5, min. reproduction size 1.

## Finding 1: a real period-2 oscillator at a tile edge ("the AT-AT")

Universe F's tile `0,1` tripped the grid-expansion logic in the `top`
direction on **every single generation from gen 1405 through gen 1431** (26
generations straight), alternating exactly between two section-count
signatures:

```
gen 1406: [0, 7, 4, 0, 11, 0, 0, 9, 0]  total 31
gen 1407: [0, 9, 4, 0,  8, 0, 0, 10, 0]  total 31
gen 1408: [0, 7, 4, 0, 11, 0, 0, 9, 0]  total 31   <- back to gen 1406's exact signature
gen 1409: [0, 9, 4, 0,  8, 0, 0, 10, 0]  total 31
...repeating exactly, every tick, through gen 1431
```

A real period-2 blinker-type structure parked on the tile boundary,
flipping phase every generation and poking across the edge on alternating
ticks - almost certainly what looked like a two-legged walker pattern
repeating in the live view.

## Finding 2: byte-identical recurring genotypes across breeding events

Breeding at gen 1305 produced three children with totals 50, 60, 60.
Breeding at gen 1488 - 183 generations later - produced three children
with totals 50, 60, 60 again, under different letters. Queried the
database directly and **byte-compared the actual frozen original tiles**
(not just population totals) behind each:

| Gen 1305 | Gen 1488 | Result |
|---|---|---|
| F (bred from C x D) | A (bred from B x E) | **identical**, 1536 bytes, bit-for-bit |
| B (bred from A x C) | D (bred from E x F) | **identical**, 1536 bytes, bit-for-bit |
| E (bred from A x D) | C (bred from B x F) | **identical**, 1536 bytes, bit-for-bit |

Not a coincidence of matching totals - the exact same three genotypes
reappeared under different letters. This confirms (with hard data, not
inference) the hypothesis from the screenshot-only investigations: the
breeding process has real fixed points, specific patterns it keeps
regenerating rather than drifting away from, independent of which of the
six slots they land in.

## How this was found

Query used (see `tools/import_snapshot.py` for the schema): pull every
`creation_events` row for the run ordered by generation, scan for repeated
`sections_json` signatures (caught the oscillator) and repeated `total`
values across different birth generations (caught the recurring
genotypes), then cross-reference `universes.origin_tile_b64`, decode both
candidates' base64, and compare the raw bytes directly.

## Files

- `../../data/gol-export-gen1488-1791096352578.json` - the source export
- `data/lab.sqlite`, `run_id=2`, `run_label='oscillation-4'` - the
  imported, queryable version of the same data
