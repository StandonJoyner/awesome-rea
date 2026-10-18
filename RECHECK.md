# RECHECK.md — the monthly look-back over what is already entered

Operating procedure only; the reader-facing product is `README.md`. Admission lives in
`INTAKE.md` (`## Admission`, tests A1–A3) and is **not** re-decided here: a recheck pass asks
whether an entry is still true, never whether a new project should be added.

`scripts/recheck.py` is the whole mechanism. It reads `README.md` for the entry bullets and
the newest `data/measurement/snapshot-<date>.tsv` for the measured numbers, so a pass costs
**zero API requests** when the snapshot is fresh — measured 2026-10-17: 131 checked
repositories in 2.0 s. It refuses to run against a snapshot older than `--max-age` days
(31 by default) rather than conclude from stale numbers, which is the mistake that produced
five phantom rows in the first prototype (the snapshot still carried the four trainer
repositories deleted from the README on 2026-10-17).

## The four triggers, and who acts on each

Each is machine-decidable, and each writes a code into the `flags` column plus the evidence
into `detail`:

| Code | Fires when | `need` | What acting costs |
| --- | --- | --- | --- |
| `gone` | the linked repository answers 404 | `fix` | one request to confirm, then the line goes or the URL is corrected |
| `stale` | ★ ≥ `--floor` (1000) and no push for `--quiet` (365) days | `read` | nothing beyond a decision: dormancy alone never removes an entry |
| `lic` | our entry line states a bare licence name the API's `license.spdx_id` does not confirm | `read` | re-read `LICENSE` once; a line that already hedges (`-style`, `with additional terms`, `if declared`, or one that names `NOASSERTION` itself) is not flagged |
| `dmca` | a notice in `github/dmca` contains both the owner and the repository token | `read` | read that one notice file |

Anything not in this table is out of scope by decision, not by oversight:

- **How full a repository's contents are is not checked, and no rule of ours governs it.** The
  only boundary rule we have is that this repository ships no game files, ROMs, cracked
  binaries or keys — it constrains our tree, not what a linked tree holds. Whether a file
  inside somebody else's repository really is the rights holder's build is something we
  cannot determine from the outside, so we do not write a test that we cannot run.
- `archived` is recorded in the snapshot but triggers nothing. It is an owner's read-only
  switch, and measured 2026-10-17 it is `false` for **all 131** linked repositories; treating
  it as a signal would mean guessing at intent.
- The four `Related lists` repositories are skipped (`alphaSeclab/awesome-reverse-engineering`,
  `user1342/Awesome-Android-Reverse-Engineering`, `morluto/awesome-reverse-engineering`,
  `SubmitGame/awesome-decomp-games`): they are boundary lists we point at, not reconstructions,
  so their push age makes no claim about a result. That is why the 2026-10-17 pass counted **131** of the
  135 repositories then linked; the number is that run's, not the corpus's.

## Output format

`data/measurement/recheck-<date>.tsv`, gitignored like every other measurement artefact, seven columns:

```
repo	status	stars	pushed	flags	detail	need
sdlpal/sdlpal	ok	1980	2026-10-05	dmca	2022-08-2022-08-30-sdlpal.md	read
n64decomp/sm64	ok	8885	2024-02-04	stale	986d	read
snesrev/zelda3	ok	4862	2026-10-02	lic	line=MIT field=NOASSERTION	read
```

- `status` is `ok`, `gone`, or `err`; `flags` is a semicolon list, empty when clean; `detail`
  carries the evidence in the same order; `need` is `fix`, `read`, or `none`.
- **Clean rows are written too.** The file is the record that a pass happened across all
  entries, not a complaint list; a file containing only hits would make a partial run
  indistinguishable from a healthy one.
- stdout prints the header line, a per-code tally, then the `need != none` rows only, sorted
  by stars descending — the printed block is the work queue, the TSV is the evidence.
- Exit `2` when more than 5% of rows are `err` (rate limit or network), so a half-finished
  pass is never read as a clean one.
- `--no-dmca` skips the notice scan, which is the slow part; `--dmca-refresh` pulls the clone.

## Running it

```console
python3 scripts/recheck.py --dmca-refresh   # once a month, with a fresh snapshot first
python3 scripts/recheck.py                  # same pass against the existing clone
```

Run `python3 scripts/verify.py refresh` first if the snapshot is not current — recheck reads
it for stars, push date and licence, and will not run on a snapshot older than a month.

The notices corpus is a **plain shallow clone** at `data/cache/dmca/`
(59 MB, 23,839 files, first clone 29 s, `git pull --depth 1` afterwards), deliberately **not
a git submodule**: a submodule would pin a third-party commit inside our published history and
make every recursive clone of a documentation list fetch a corpus of legal filings. The
`github/dmca` repository is third-party data, and the same reasoning that kept the census
dumps out of the tree (`AGENTS.md`, `## Repository layout`) keeps this out.

Matching is the part that needed measuring, not the fetching. Three candidate rules, tried
against the real corpus:

- `github.com/{owner}/{repo}` verbatim: **1 file matched**, and `github.com/yuzu-emu/yuzu`
  matched none although `yuzu` appears in 27 notices — a notice lists the forks and mirrors
  that were removed, not the canonical URL. Recall near zero, so useless.
- repository name alone: catastrophic. Our short names are English fragments — `tp` hit
  374,218 times, `key` 1,822, `mm` 204.
- **repository name and owner token in the same file** — the rule shipped. Over 131 entries it
  returns 3 rows in 2 s, and each is annotated `[weak: no github.com/owner/repo]` when the
  notice does not name our exact URL, which tells the reader how attributable the match is
  before they open anything.

## What an agent does with a flagged row

The script decides *which* rows are worth attention; an agent reads only those, and only the
one artefact the `detail` column names. The point of the budget is that a monthly pass should
cost a few hundred tokens of context, not a sweep.

- `need=none` rows are never opened. They exist in the TSV as proof of coverage.
- `stale` needs no reading at all — the answer is already known (the project is quiet), so the
  action is editorial: state the push date in the line if it is not already there. An agent
  asked to review a `stale` row should do nothing beyond checking the line.
- `dmca` opens **the one file named in `detail`**, and only the lines carrying the repository
  name (`grep -n -i -A3` on the notice, not a whole-file read; notices run to hundreds of lines
  of boilerplate). A `[weak…]` marker means the notice does not name our URL, so one confirming
  grep closes it as noise.
- `lic` opens `LICENSE` at the repository root — the header lines only, to see whether it is a
  stock text with added terms — and stops. Never re-read a README for a licence question.
- `gone` is the only code that may need a second API call, and it has already spent it.
- One fact per row goes back into a file: a legal or provenance fact into this document,
  `AGENTS.md` or `INTAKE.md`, a wording fix into the entry line. An agent that finds nothing writes one clause
  saying so; it does not justify a non-finding.
- The cap is the row count, not the clock: a pass with 16 actionable rows is 16 bounded reads.
  If `need` rows ever exceed about 40, the pass is too wide — narrow `--floor`/`--quiet` or
  batch it, rather than letting an agent walk the corpus.

## What the first pass found, 2026-10-17

131 repositories, 16 rows with `need != none`: 11 `stale`, 2 `lic`, 3 `dmca`. The `stale` set
is the expected one — `diasurgical/devilution`, `n64decomp/sm64`, `k4zmu2a/SpaceCadetPinball`,
`wheybags/freeablo`, `in0finite/SanAndreasUnity`, `sm64pc/sm64ex`, `alexbatalov/fallout1-ce`
and `-ce`, `yvt/openspades`, `sgan81/apfs-fuse`, `collinsmith/riiablo` — and none of them is a
candidate for removal, only for a status phrase in the line.

The three `dmca` rows each resolved to a different fact, which is why the flag means *read*,
not *delete*:

- `sdlpal/sdlpal` → `2022-08-2022-08-30-sdlpal.md`. The complainant identifies as an SDLPAL
  maintainer and targets **modified builds linked against proprietary advertising SDKs**, a
  GPL-violation action against derivatives. Nothing in the notice alleges that the
  reimplementation itself infringes.
- `OpenSC2K/OpenSC2K` → `2018/2018-07-25-EA-2.md` and `2018-11-2018-11-16-EA-CounterNotice.md`:
  EA's own counter-notice text states the repository does not infringe.
- `OpenRA/OpenRA` → noise, correctly marked `[weak…]`: the file names the unrelated
  `KOYK/OpenRA-Tiberian-Dawn-Apolyton`.

The two real ones are legal-record material and are written up in `AGENTS.md`
`## Takedown and legal record`; whether either is a reason to **remove** an entry is decided by
the four reasons in `AGENTS.md` `## Removal`, not here. The `lic` rows (`snesrev/zelda3`, `LoreanXavier/pt-pc`) are the
cases the hedge rule keeps: both lines say plain `MIT` while GitHub's classifier reports
`NOASSERTION`, so the licence file exists but is not a stock text — worth one clause in the
line, not an argument.
