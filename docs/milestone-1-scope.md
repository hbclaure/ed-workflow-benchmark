# Milestone 1: working scope

Version 0.1 · November 1, 2026. Scope and starting searches are ready; literature discovery is next. Operational rules below are provisional defaults to refine and log as discovery reveals ambiguities.

| Decision | Accepted scope |
| --- | --- |
| Research question | What activities and workflows do clinical and support personnel perform in emergency departments? |
| People | All ED personnel, including clinicians, technicians, transport, environmental services, logistics, security, and administrative staff. |
| Setting | Hospital EDs; adult and pediatric care; all countries. |
| Activities | Physical, cognitive, communication, coordination, documentation, and clinical work. |
| Evidence | Observational and time-motion studies, interviews, workflow analyses, and relevant protocols/guidelines. |
| Boundaries | Include ED-linked work; exclude unrelated hospital work. Robot capabilities and feasibility do not determine eligibility. |
| Search limits | No initial date, geography, adult/pediatric, or language filter. |

## Working defaults for eligibility and evidence

- Retain sources describing an explicit personnel activity linked to ED work. For mixed settings, use only separately identifiable ED evidence. Exclude sources with no separable ED activity information and record that reason.
- Label each activity, rather than the entire paper: **documented practice** (observed or reported), **prescribed practice** (protocol/guideline instruction), or **hypothetical/proposed** (explicitly suggested in the source). Keep documented and prescribed entries distinguishable in the core inventory. Store source-supported proposals separately in a hypothesis register. Never retain model-invented activities.
- Require a supporting passage and a retrievable location: page, section/paragraph, table/row, or abstract sentence. Do not infer component tasks, actors, objects, or sequence. Mark missing details as unknown.
- At initial screening, retain uncertain cases for closer assessment. Inaccessible full text means **awaiting retrieval**, not automatic exclusion. Translations are permitted; record language and translation method, and check the supporting passage against the original before verification. Flag unresolved translation uncertainty.
- Record clear exclusions using specific reasons: wrong setting/no separable ED evidence, no personnel activity described, or duplicate record. Preserve duplicate identifiers and retrieval provenance.

## What will be recorded later

Minimum activity fields: activity ID; source ID and DOI/PMID when available; evidence label; actor; action/task; objects; ED location; workflow when stated; exact supporting passage; source location; verification status. Unknown fields stay explicit. Retain extraction model/prompt versions and run identifiers.

Provisional granularity: a **workflow** coordinates activities toward a broader outcome; a **task** is a goal-directed activity with an identifiable outcome; a **skill** is a reusable action/capability. Preserve the source's detail; these definitions do not authorize decomposing a task into unstated steps.

## Next milestone: agent-led literature discovery

The agent will search PubMed using the starting streams below, inspect results, expand terminology, follow citations, and use OpenAlex for complementary discovery. It will also seek relevant guidelines/protocols on issuing organizations' sites, retaining the organization, version/date, and URL. No manual literature-finding step is required. These are exploratory starting searches, not a validated final search strategy.

**Activities, workflow, and cognitive/communication work**

```text
("Emergency Service, Hospital"[mh] OR "emergency department*"[tiab] OR "emergency room*"[tiab]) AND ("Time and Motion Studies"[mh] OR "time motion"[tiab] OR "time and motion"[tiab] OR workflow*[tiab] OR "work sampling"[tiab] OR "task analysis"[tiab] OR "work activities"[tiab] OR communication[tiab] OR coordination[tiab] OR documentation[tiab] OR "decision making"[tiab])
```

**Support and logistical work**

```text
("Emergency Service, Hospital"[mh] OR "emergency department*"[tiab] OR "emergency room*"[tiab]) AND (transport*[tiab] OR restock*[tiab] OR clean*[tiab] OR "environmental services"[tiab] OR "support staff"[tiab] OR "supply management"[tiab] OR clerical[tiab] OR security[tiab])
```

**Prescribed activities in guidelines/protocols**

```text
("Emergency Service, Hospital"[mh] OR "emergency department*"[tiab] OR "emergency room*"[tiab]) AND ("Practice Guideline"[pt] OR "Guideline"[pt] OR guideline*[tiab] OR protocol*[tiab])
```

For every search/citation route, retain database, exact query, execution date, result count, identifiers, and discovery route. Save screening decisions/reasons and log query or scope revisions. Keep agent model/prompt versions. Discovery output will be a deduplicated candidate register with retained, excluded, uncertain, and awaiting-retrieval statuses; activity extraction follows later.

PubMed ESearch syntax check, November 1, 2026: all three queries were accepted without errors or warnings, returning 16,576, 7,939, and 24,067 matches respectively. Counts overlap. No paper records were retrieved or screened during this check.

Method references: [PubMed search syntax](https://pubmed.ncbi.nlm.nih.gov/help/) and [JBI inclusion-criteria guidance](https://jbi-global.atlassian.net/wiki/spaces/MANUAL/pages/355862707/10.2.4%2BInclusion%2Bcriteria).
