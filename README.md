# Cellular Automaton — Emergent Behavior Lab

A browser-based Conway's Game of Life sandbox, built up iteratively as an
experiment in emergent behavior — starting from a standard single-grid
implementation and growing into a six-universe breeding ecosystem.

Open `index.html` directly in a browser. No build step, no dependencies —
it's a single self-contained HTML file.

## What it does

- **Standard Game of Life controls**: click/drag to paint cells, step,
  run/pause, randomize, clear, reset, adjustable speed and grid size.
- **Infinite tiling**: when a pattern grows past its grid's edge, a new
  same-size grid is created next to it (with auto-pause and a ghost preview
  of what will be created), seeded from the overflowing edge — unless that
  edge falls short of a configurable minimum reproduction size, in which
  case it warps to the opposite edge of its own grid instead.
- **3x3 subdivision**: every grid is visually divided into a symmetric 3x3,
  and starting cells may only be hand-placed in the center cell. A new grid's
  center is seeded from whichever of its parent's edge-thirds overflowed.
- **Lifespan & stall pruning**: a grid can be configured to die off after a
  fixed number of generations, or once the trend line through its recent
  population (least-squares slope) goes flat — catching settled oscillators,
  not just true still lifes.
- **Six parallel universes (A–F)**, stepped in lockstep on a shared
  generation counter. Each is independent until one dies out completely —
  then it drops out of the lineup.
- **Breeding**: once only three universes remain alive, the run auto-pauses
  and breeds every pairwise combination of the three survivors — XOR of each
  parent's *original* (frozen-at-birth) starting pattern, never its evolved
  state — back into the empty slots, refilling the lineup to six. If more
  than one death happens in the same tick and that undershoots three
  survivors, the longest-lived of that tick's casualties are pulled back in
  by their own original pattern to round the parent pool back out to three.
- **Population graph tab**: a rolling line chart per universe, tracking every
  grid's population generation by generation, plus a creation log recording
  each new grid's parent, direction, and 3x3 section counts at the moment it
  was born.

## What we found

Because Conway's rule and the XOR breeding step are both fully
deterministic, and the only randomness in the whole system is a single
"Random" click at the start, the six-universe ecosystem is a deterministic
dynamical system over a finite state space — which means it's mathematically
guaranteed to eventually cycle. In practice it does, and fast:

- One seed settled into an exact **period-2** cycle almost immediately:
  universes {A, C, E} and {B, D, F} simply swapped which trio was "alive"
  each breeding round, with bit-identical population curves reappearing
  every other breed.
- A second seed turned out messier at first glance — the alive/dormant
  letter groupings didn't repeat on the same schedule — but turned out to be
  an exact **period-3** cycle once tracked all the way through (Breed 3
  reproduced Breed 0's values exactly, universe for universe). The letters
  the pattern rode in on had rotated between breeds, which is what made it
  look aperiodic before the full period closed.

Screenshots and notes from both runs are in `analysis/`.

## Recording data to the database

Screenshots work for a quick look, but get hard to compare precisely once
you're tracking lineage across many breeding cycles. There's now a proper
path to structured, queryable data instead:

1. Click **Export data** in the page. It downloads a JSON file with the
   full current state — every universe's live tiles, birth/death
   generations, population history, and creation log (including breed
   events, with each child's exact parent pair).
2. Import it into the lab's SQLite database:
   ```
   python tools/import_snapshot.py --run <label> path/to/gol-export-....json
   ```
   `<label>` groups related exports together (e.g. `oscillation-3`) so you
   can capture the same run at several points in time and query across all
   of them. Each import adds a new `runs` row rather than overwriting
   anything, so nothing is lost by exporting too often.
3. The database lives at `data/lab.sqlite` (created on first import) with
   tables for `runs`, `universes`, `tiles`, `creation_events` (every grid
   creation and breed event, with parent pairs for bred ones), and
   `population_samples` (full generation-by-generation history per tile).
   Query it directly with Python's `sqlite3` module, or any SQLite client.

This is what lets lineage questions (e.g. "does this population-71 newborn
always trace back to the same two parent letters?") get answered by a
query instead of by eyeballing screenshots.

## Project history

Built conversationally, feature by feature, in a Claude Code session — see
`analysis/` for the oscillation investigation that prompted turning this
into its own repo, and `data/lab.sqlite` (once populated) for the
structured version of that same investigation.
