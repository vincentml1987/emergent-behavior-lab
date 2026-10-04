# Run 5 — first run at BREED_THRESHOLD=4 (10 universes)

Export at gen 2192 (`data/gol-export-gen2192-1791097232042.json`), imported
as run label `oscillation-5`, `run_id=3` in `data/lab.sqlite`.

## Confirmed: a real recurring genotype, spotted by eye first

Teddy flagged a repeating multi-tile population signature in Universe I's
graph (spike, then several tiles lock flat almost simultaneously) -
screenshot in `repeating-shape-flagged.png`. Queried the database for
duplicate `creation_events` section signatures and found Universe I's
current origin (born gen 2192, bred from E x G, population 66) shares its
exact signature with Universe B's origin from gen 1967 (bred from A x D).

Byte-compared the two origin tiles directly:

```
B (born 1967) vs I (born 2192): IDENTICAL
```

225 generations apart, same pattern, confirmed bit-for-bit - not just a
population match. Third confirmed real recurrence now (after the two from
`oscillation-4`), and the first one caught starting from a visual
observation rather than a database query.

## Caution: a 4-way "match" that wasn't

The same search also surfaced four creation events all totaling population
67: A (gen 2192, bred B x E), D (gen 2192, bred B x G), E (gen 1967, bred
A x I), G (gen 1967, bred D x I). Tempting to call this a bigger recurring
cluster than the B/I pair. Byte-comparing all six pairs showed it's
actually **two different patterns that happen to share a population
total**:

```
A vs G: IDENTICAL
D vs E: IDENTICAL
A vs D, A vs E, D vs G, E vs G: all different
```

Same lesson as the premature "period-3" call in `oscillation-3`: a
matching population total is a lead, never confirmation by itself. Always
byte-compare `origin_tile_b64` before calling something a true recurrence.

## Files

- `repeating-shape-flagged.png` - the screenshot that started this
- `../../data/gol-export-gen2192-1791097232042.json` - the source export
- `data/lab.sqlite`, `run_id=3`, `run_label='oscillation-5'`
