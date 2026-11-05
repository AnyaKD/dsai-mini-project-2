# Client brief

*[Fictional — for coursework only. Replace the names with real ones only if you
have a real client.]*

---

## The client

**Kāinga Ora — Homes and Communities**

New Zealand's public housing agency. It owns and manages state housing, runs
urban regeneration programmes, and partners with community housing providers and
councils. It is also the agency that carries the statutory responsibility for
housing supply and for addressing severe housing deprivation.

**Why they would commission this.** Their need assessment, their investment
decisions and their reporting against housing outcomes all depend on
*small-area* evidence. The households with the most acute need are, by
definition, the ones least served by a direct measurement — no administrative
file covers them cleanly, and survey samples are too thin once you cut them to a
suburb. The census is the one source with near-universal coverage at SA2 level.

**A second reader, and the more interesting one.** The **Ministry for Cities,
Environment, Regions and Transport (MCERT)** sets the policy settings Kāinga Ora
then delivers against. MCERT was established in 2026 and brings together the
functions of four former agencies — the Ministry for the Environment, the
**Ministry of Housing and Urban Development (HUD)**, the Ministry of Transport,
and local government functions from the Department of Internal Affairs. HUD
became part of MCERT on 1 July 2026, so the housing and urban development
portfolio now sits inside a much larger ministry alongside transport, the
environment and regional development.

Their people will read the same deck as an invited guest, and they care about a
different sentence: not "where is crowding worst" but "are the boundaries we
plan against the right ones". That second question is what makes this project
more than a heat map, and it is why the cluster-versus-administrative comparison
is in it.

The merger is quietly relevant to the project. MCERT's own framing is about
joining up the levers that shape how people "live, move, build, grow and
protect" — and a statistical geography that cuts across transport, environment
and housing concerns at once is exactly the kind of evidence a combined ministry
has to reason with.

## The commission

> We need a defensible way of finding and monitoring crowded households at
> small-area level, because our current indicators are too coarse to allocate
> against.
>
> We can see crowding in the census, but only after the fact and only in the
> areas we already suspected. We want to know whether the same census variables
> that sit alongside crowding can carry the signal on their own — so that
> monitoring does not depend on measuring crowding directly every time.
>
> And while we are asking: our planning and reporting use territorial authorities
> and regional councils. Those are administrative lines. We have no evidence they
> group areas that are actually alike. If areas with similar profiles can be
> grouped from the data instead, we need to know how far that grouping differs
> from the boundaries we plan against — and whether it predicts crowding better.
>
> **What we need from you:** an honest answer to how well this works, and a clear
> statement of what it cannot tell us. We would rather have a modest result we can
> rely on than an impressive one we cannot.

## The individuals

*[Fictional — fill in or replace.]*

- **Hine Ngata** — Senior Analyst, Housing Supply & Evidence, Kāinga Ora.
  Commissioned the work. Wants defensible numbers she can put in front of a
  funding panel.
- **Tom Whitcombe** — Senior Data Analyst, same team. Your day-to-day contact,
  and the technical reader who will check the metric choice. Reads the README
  before the deck.
- **Dr Sarah Chen** — Principal Advisor, Housing Analytics, MCERT. The invited
  guest. Will ask whether area-level inference says anything about individual
  households — she has asked it before and been given a bad answer. Former HUD,
  now in the merged ministry.
- **Marcus Reweti** — Regional Planning Lead, Kāinga Ora. Practical reader.
  Will ask "does this change a decision I make?" within the first two minutes.

## Why 2023, and not something more recent

A fair question to ask before starting, and the answer is not "it was the latest
download that worked".

**There was no 2025 census.** In June 2025 the Government announced that New
Zealand's five-yearly field enumeration would end. The next census moves from
2028 to **2030**, and the model changes from survey-first to **admin data-first**:
administrative data already collected across government becomes the backbone,
supported by an annual Census Attributes Survey — starting in 2027 and sampling
a few percent of the population each year — that fills the gaps admin data
leaves. This is legislative, not a plan: the **Data and Statistics (Census)
Amendment Bill** moves the next census to 2030 and requires annual publication
from then.

October 2025 *was* a census event, but a field **test** only — around 1,850
households across New Plymouth, Christchurch and Ashburton, explicitly not used
to produce official statistics. It tested data flow through the systems, nothing
more.

**So 2023 is the most recent census, and the last of its kind.** For a crowding
question at SA2 level that makes it not merely the latest available source but
the only one that will ever exist in this form.

**Why that matters to this project specifically.** Household crowding is derived
from household composition measured against a bedroom requirement. That is
questionnaire-shaped information: admin data does not capture it the way a census
form does. The same concern has been raised publicly about adjacent measures —
in the debate over replacing the census, the areas flagged as most exposed to
"holes" under admin data included homelessness, which sits in the same family as
crowding.

Three practical consequences:

1. **The baseline is a one-off.** It cannot be refreshed on the same basis, so
   any monitoring built on it needs a stated plan for the 2030 transition rather
   than an assumption of a 2028 refresh.
2. **The limitation has a horizon, not just a caveat.** The README's
   data-availability note isn't the usual "the data is a snapshot" line. It is a
   specific statement that the measurement instrument is being replaced.
3. **It sharpens the client's reason to care.** MCERT inherits the housing
   portfolio *through* the census transition. A defensible small-area baseline on
   the last full census, with the measurement gap named rather than glossed, is
   more useful to them than the same analysis done in an ordinary year.

**One live caveat, worth a footnote.** The 2030 date and the admin-first model
are the current legislated position, not settled reality. Reporting in August
2026 noted Stats NZ working on contingency options as the enabling legislation
moved through the House, and whether any form of count could still happen before
2030 has been raised as a question for after the next election. A policy reader
will know this. Say it in the README rather than letting the deck sound more
certain than the situation is.

Sources: [Stats NZ — Modernising the census](https://www.stats.govt.nz/census/modernising-the-census) ·
[RNZ — five-yearly census to be scrapped from 2030](https://www.rnz.co.nz/news/politics/564470/five-yearly-census-to-be-scrapped-from-2030-replaced-with-administrative-data-annual-surveys) ·
[Data and Statistics (Census) Amendment Bill](https://www.legislation.govt.nz/bill/government/2026/0253/latest/whole.html) ·
[Stats NZ — testing begins on the new census survey](https://www.stats.govt.nz/news/testing-begins-on-new-zealands-new-census-survey/)

## The question, as it reached you

Your brief, third hand, was one line: *"Can the census tell us where the crowded
households are, in areas small enough to act on?"*

That is the level of detail most briefs actually arrive with. Turning it into
something answerable is the first piece of the job, and the four blanks you have
to fill are the standard ones:

| Blanks to fill | Your answer |
|---|---|
| **Unit of analysis** | The SA2 (suburb or rural community), not the household |
| **Outcome to predict** | Household crowding index, collapsed to crowded / not |
| **Comparison to beat** | Predicting the base rate, then predicting from TA and region |
| **Decision it informs** | Where to prioritise need assessment and monitoring |

## What the client cares about, and what that means for the analysis

**They care that the ordering is right, not that the score is high.** A model
with modest recall that ranks the worst areas correctly is more useful to them
than a high-accuracy model that is accurate because it predicts "not crowded"
almost everywhere. This is why the metric is recall on the crowded class and
PR-AUC — not accuracy.

**They care about false negatives.** A crowded household the model misses is a
household that does not appear on a list and does not get assessed. The reverse
error means an assessor visits a household that turns out fine. The asymmetry
runs opposite to how it usually does, and the metric choice should say so in
those terms.

**They care about the boundaries question.** Regional planning and HUD reporting
are both organised around administrative geographies. Evidence that those
boundaries do not correspond to how areas actually differ is directly useful to
them — and evidence that they *do* correspond is equally useful, because it
justifies leaving the current arrangements alone. A null result is a deliverable
here, which is why the ARI comparison is reported however it comes out.

**They care about what it cannot do.** Specifically, that an area-level model
says nothing about an individual household. Dr Chen's question. This goes in the
README as the leading limitation and gets *said out loud* in the presentation,
not buried on the last slide.

## Headline for the README

*[Fill in from notebook 05. One sentence, in the client's terms, not the
model's.]*

Example of the shape:

> Census variables predicted household crowding across 2,379 SA2s with a recall
> of **__** and PR-AUC of **__**, against a base rate of **__**. Data-driven
> area clusters overlapped regional council boundaries only weakly
> (ARI = **__**), and adding the cluster label to the model [improved / did not
> improve] recall by **__** percentage points.

## The deck

`MP2_presentation.pptx` — 9 slides, report-readout structure, speaker notes on
every slide. It is written for Hine, with Dr Chen in the room. Numbers are
placeholders until the notebooks have run; the notes say which slide each one
comes from.
