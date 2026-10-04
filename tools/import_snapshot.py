#!/usr/bin/env python3
"""Import a Game of Life "Export data" JSON file into the lab's SQLite
database (data/lab.sqlite), tagged under a run label.

Usage:
    python tools/import_snapshot.py --run oscillation-3 path/to/export.json

Each import is additive: it records a new row in `runs` and attaches all
of that export's universes/tiles/creation-events/population-samples to it,
so the same run label can be imported multiple times (e.g. once per
breeding cycle you capture) without overwriting earlier imports. Query
across every captured moment of a run by joining on run_label.
"""
import argparse
import base64
import json
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY,
    run_label TEXT NOT NULL,
    source_file TEXT NOT NULL,
    exported_at TEXT,
    imported_at TEXT DEFAULT (datetime('now')),
    cols INTEGER, rows INTEGER, gen INTEGER,
    auto_pause INTEGER, gen_limit INTEGER, stall_limit INTEGER,
    stall_tolerance REAL, min_repro INTEGER
);

CREATE TABLE IF NOT EXISTS universes (
    id INTEGER PRIMARY KEY,
    run_id INTEGER NOT NULL REFERENCES runs(id),
    letter TEXT NOT NULL,
    born_at_gen INTEGER,
    died_at_gen INTEGER,
    origin_tile_b64 TEXT,
    origin_population INTEGER
);

CREATE TABLE IF NOT EXISTS tiles (
    id INTEGER PRIMARY KEY,
    universe_id INTEGER NOT NULL REFERENCES universes(id),
    tile_key TEXT NOT NULL,
    born_at_gen INTEGER,
    population INTEGER
);

CREATE TABLE IF NOT EXISTS creation_events (
    id INTEGER PRIMARY KEY,
    universe_id INTEGER NOT NULL REFERENCES universes(id),
    gen INTEGER,
    new_tile TEXT,
    source_tile TEXT,
    direction TEXT,
    sections_json TEXT,
    total INTEGER
);

CREATE TABLE IF NOT EXISTS population_samples (
    id INTEGER PRIMARY KEY,
    universe_id INTEGER NOT NULL REFERENCES universes(id),
    tile_key TEXT NOT NULL,
    gen INTEGER NOT NULL,
    population INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_pop_samples_lookup
    ON population_samples(universe_id, tile_key, gen);
CREATE INDEX IF NOT EXISTS idx_creation_events_universe
    ON creation_events(universe_id, gen);
"""


def decode_population(b64):
    if not b64:
        return 0
    return sum(base64.b64decode(b64))


def import_file(conn, run_label, path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))

    cur = conn.execute(
        """INSERT INTO runs
           (run_label, source_file, exported_at, cols, rows, gen,
            auto_pause, gen_limit, stall_limit, stall_tolerance, min_repro)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            run_label, str(path), data.get("exportedAt"),
            data.get("cols"), data.get("rows"), data.get("gen"),
            int(bool(data.get("autoPause"))), data.get("genLimit"),
            data.get("stallLimit"), data.get("stallTolerance"), data.get("minRepro"),
        ),
    )
    run_id = cur.lastrowid

    uni_keys = [k for k in data.keys() if k.startswith("uni") and len(k) == 4]
    for key in sorted(uni_keys):
        letter = key[3]
        uni = data[key]
        origin_b64 = uni.get("originTile")
        cur = conn.execute(
            """INSERT INTO universes
               (run_id, letter, born_at_gen, died_at_gen, origin_tile_b64, origin_population)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                run_id, letter, uni.get("bornAtGen"), uni.get("diedAtGen"),
                origin_b64, decode_population(origin_b64),
            ),
        )
        universe_id = cur.lastrowid

        tile_birth = uni.get("tileBirth") or {}
        tiles = uni.get("tiles") or {}
        for tile_key, b64 in tiles.items():
            conn.execute(
                """INSERT INTO tiles (universe_id, tile_key, born_at_gen, population)
                   VALUES (?, ?, ?, ?)""",
                (universe_id, tile_key, tile_birth.get(tile_key), decode_population(b64)),
            )

        for ev in uni.get("creationLog") or []:
            conn.execute(
                """INSERT INTO creation_events
                   (universe_id, gen, new_tile, source_tile, direction, sections_json, total)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    universe_id, ev.get("gen"), ev.get("newTile"), ev.get("sourceTile"),
                    ev.get("direction"), json.dumps(ev.get("sections")), ev.get("total"),
                ),
            )

        pop_history = uni.get("popHistory") or {}
        for tile_key, points in pop_history.items():
            conn.executemany(
                """INSERT INTO population_samples (universe_id, tile_key, gen, population)
                   VALUES (?, ?, ?, ?)""",
                [(universe_id, tile_key, p.get("gen"), p.get("pop")) for p in points],
            )

    conn.commit()
    return run_id, len(uni_keys)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", required=True, help="Run label, e.g. oscillation-3")
    parser.add_argument("--db", default=str(Path(__file__).resolve().parent.parent / "data" / "lab.sqlite"))
    parser.add_argument("export_json", help="Path to a gol-export-*.json file")
    args = parser.parse_args()

    Path(args.db).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.db)
    conn.executescript(SCHEMA)

    run_id, n_universes = import_file(conn, args.run, args.export_json)
    print(f"Imported run_id={run_id} run_label={args.run!r} ({n_universes} universes) into {args.db}")


if __name__ == "__main__":
    main()
