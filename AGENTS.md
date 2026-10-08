# AI conventions

## About this repository
This public portfolio belongs to Meghan Hernandez, a University of Hawaii at Manoa BBA student in Finance.
Canonical file: AGENTS.md. CLAUDE.md points here.

## Where things are
- README.md             who I am + the index of engagement
- RESUME.md             
- AGENTS.md             canonical AI conventions
- CLAUDE.md             pointer to AGENTS.md
- prompt-log.md         running record of AI sessions that mattered
- .gitignore            files that must never enter the history
- capabilities/         one folder per capability
- capabilities/marginal-analysis/  capability description and method specification; model.xlsx will be added by Meghan
- docs/briefs/          written BEFORE the work: scope + hypothesis
- docs/decisions/       written AFTER the work: recommendations to an audience
- data/                 sourced inputs, with provenance
- analysis/             findings
- analysis/figures/     charts the findings refer to
- models/               Performance Ratios only
- models/templates/     Performance Ratios templates
- models/builds/        Performance Ratios builds

## Naming
- The directory matters most. A file in the wrong folder is harder to find. If you are not certain which folder a file belongs in, ask me
  before you write it — do not choose for me.
- Graded files use the exact filename the stage brief gives — lowercase,
  hyphens, no spaces. Dated documents are YYYY-MM-DD-slug-type.md (no name — the repo is yours);
  the stage page says so when they do.
- Slugs name the engagement, never the week, the course, or the assignment
  number.
- Never invent a path or a filename. I will give you the exact one.

## How I work
- Explain finance and business concepts fully, and walk through worked examples. Do not hand me conclusions.
- Critique my reasoning directly; I would rather be corrected than agreed with.
- When uncertain, say so and explain what would resolve the uncertainty.
- Explain jargon in plain language while retaining the precise terms I need to learn.
- If the brief is ambigous, say so and stop - don't invent the scope.
- No made-up numbers, sources, or experience. Missing data gets a `<placeholder>` and a note, not a plausible-looking value.

## What you may and may not draft
- You MAY explain, critique, debug, quiz me, and draft mechanical files.
- You MAY NOT write my briefs, analyses, memos, or reflections.
- Every statistic or figure is a draft until I verify it against a source.

## Documentation
When work changes, update the document that describes it in the same commit.
A capability's README names the engagements that exercised it; keep that current.

## Scope
Do the work I asked for. If you notice something worth doing that I did not ask for, tell me instead of doing it.

## Commits
Descriptive messages: what changed and why. Never "update" or "stuff".

## Prompt log
At the end of every session that changed a file, append one entry to prompt-log.md: the date, what I asked, what you produced, what was wrong and how it was caught. Never backfill earlier sessions and never edit a past entry.

## Never include or paste into a model
This repository is public, and anything unsafe for public release must not be pasted into a model either. Never include:
- Resident names, contact details, addresses, identification, case notes, care plans, disability or health information, medication details, or other records from direct-support work.
- Student names, IDs, contact information, housing/residential records, package or mail tracking details, or other student records from campus work.
- Lockout reports, key-control records, key codes, access credentials, or other residential security details.
- Customer records, payment-card details, transaction-level personal information, or staff personal information from food-service work.
- Private volunteer, shelter, youth, or family records and identifying details.
- Credentials, API keys, or personal data about anyone.

If one of these appears in material provided to you, stop and tell me rather than including it in repository content. If sensitive material is pushed, do not assume a later deletion removes it from history; ask my instructor for help.

## Language
Whatever language I use with an AI, work handed in for this portfolio must be in English.

## Mistakes to avoid
- (empty — add the first one when it happens)
