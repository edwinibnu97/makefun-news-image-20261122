// Entry runner for make.fun news-image-20261122 (Node 22, stdlib only).
// The front page is baked into this repo as entry.png (see generate.py);
// this program drops a copy at the grader's output directory.
// Deterministic: same bytes in, same bytes out, every run.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
writeFileSync(
  join(outDir, "entry.png"),
  readFileSync(join(here, "entry.png")),
);
