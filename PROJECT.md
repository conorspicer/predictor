# The NFL Predictor idea

This describes the behavior in the preserved source, rather than proposing a new
product. The original pre-fix code is at commit `88e5808`; the security and
compatibility work lives in a separate review branch.

## The game

Four friends predict the home and away score of each NFL fixture. They compare
weekly points and a season leaderboard, choose playoff teams and Super Bowl
finalists, and keep a Hall of Fame of past winners and their prize jerseys.
The preserved UI names conorspicer, torinmehmet, magnusmartinsen and lewismead.

A fixture stores its teams, week, kickoff time, actual scores and `changeable`
flag. That flag is used as an active-season marker, not a record of whether a
game has finished. A pick links one player to a fixture and stores two predicted
scores and a `lock` checkbox. Match scores are entered manually; the score-update
management command in the source is empty.

The weekly prediction editor shows the current week's active fixtures. Its own
help text says picks close about one hour before kickoff. The old implementation
actually accepted edits five hours afterwards and other list pages exposed picks
early. The repair enforces the documented deadline, validates it on submission,
and reveals other players' picks at that same boundary. Personal pick history
remains visible to its owner.

## Scoring retained from the source

For a played game with a complete prediction:

| Component | Points |
| --- | --- |
| Correct winning team, or correctly predicted tie | 25 |
| Accuracy of the absolute winning margin | max(10 - absolute margin error, 0) |
| Accuracy of the combined score | max(10 - absolute total-score error, 0) |

An exact score earns 45 points. A wrong winner can still earn margin and total
points: predicting 30–20 away instead of an actual 20–30 has the same absolute
margin and combined score, so earns 20. This is existing behavior.

The SQL leaderboard substitutes a 30–20 home win for blank predictions. The Python
pick properties instead return zero points for missing predictions. Both behaviors
are documented and retained; there is no evidence here for choosing a replacement
rule. The `lock` checkbox is stored and displayed but does not multiply points in
either scoring implementation. Its intended additional rule is unknown.

The source considers kickoff timing when calculating points; it has no separate
final-game status. The results detail page waits four hours after kickoff. Actual
scores therefore still need to be maintained by a scorekeeper.

## Weeks and season setup

Week rollover is Wednesday at 05:00 UTC, capped at week 22. The repair derives its
starting date from the active week-one fixtures, or from `SEASON_WEEK_ONE_END`.
Previous-season fixtures need `changeable=false`. The demo schedule is fictional
and relative to the time it is created; it is not a current NFL feed.

The original app used manually provisioned rows for each player and week in
`results_userweekresult`, and a row per player in `UserTotalResult`. SQL views join
those rows to computed pick scores. The demo command provisions these explicitly.

Playoff choices include each division winner, three wildcards per conference and
the Super Bowl winner and runner-up. Form choices restrict divisions/conferences.
The source does not implement playoff scoring, a playoff submission deadline,
uniqueness between selected teams, or automatic playoff-row creation at signup.
A player without a provisioned playoff row now receives a 404 instead of a crash.

## Boundaries of the preservation

- The four named player columns remain. Adding arbitrary players needs a separate
  design decision; signup alone does not provision their entire season.
- The historical setup scripts are retained as reference. Some are incomplete or
  misnamed; `seed_demo` is the supported path for a clean fictional example.
- The existing design, logos, Hall of Fame and original scoring are kept.
- No historic account export, live service or production migration is needed.
- No Git history is rewritten and no production deployment is performed.

## Evidence

The automated suite checks expected score vectors in both Python and the actual
SQL views, including ties, shutouts, wrong winners and the `lock` flag. It checks
blank defaults, early/late fixtures, editable and closed picks, form ownership,
permissions, signup, password compatibility, playoff forms, image uploads, and a
fresh demo's page set. GitHub runs it on both SQLite and MySQL.

These checks support compatibility of the exercised paths. They do not establish
rules for the unfinished features or claim that every legacy setup script works.
