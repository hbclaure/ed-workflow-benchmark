# ED activity research pipeline

Starter Python environment for literature discovery, evidence-based activity
extraction, and catalog development. Research scope and eligibility decisions
are defined in milestone 1 before implementing the pipeline.

The [milestone 1 working scope](docs/milestone-1-scope.md) records the scope,
eligibility rules, evidence labels, and starting queries. Literature discovery
in the next milestone is agent-led; no manual paper-finding step is required.

Running `1_literature_collector.py` saves the current run's cumulative paper records to
`output.json` and appends each search response to `search_log.jsonl` (one JSON
object per line). Search entries include the exact query, UTC timestamp, total
matches, returned PMIDs, and request settings. Each paper's `SearchIDs` links to
all searches that found it. Within each run, repeated PMIDs reuse an existing
paper record before downloading, while retaining every query and search ID.
The log preserves
previous runs; returned PMIDs describe search results, not completed downloads.

The parser supports both journal articles (`PubmedArticle`) and book chapters
(`PubmedBookArticle`). `RecordType` identifies the XML layout, and `BookTitle`
holds the enclosing book's title when present. For chapters, `PubDate` is the
book publication date; contribution and indexing dates are distinct. Identifiers
are read from the record's own metadata, so cited papers' DOIs/PMCIDs are excluded.

Set `EXPORT_CSV = True` near the top of `1_literature_collector.py` to also save
`output.csv` after each query. Set it to `False` to save JSON only; an existing
CSV is left untouched. Each CSV row represents one paper. All fields are
included, with nested dictionaries expanded into columns such as `PubDate.year`.
Lists, including authors and abstract sections, are preserved as JSON text in
individual cells. Missing values and JSON nulls appear as blank cells.

To convert an existing JSON file without running searches:

```sh
python csv_export.py output.json output.csv
```

Other scripts can call the same function:

```python
from csv_export import export_json_to_csv

export_json_to_csv("experiment_1_output.json", "experiment_1_output.csv")
```

## Activate the environment

From the project directory:

```sh
source .venv/bin/activate
python --version
```

The initial environment uses Python 3.13.13. Activation applies to the current
terminal session. Use `deactivate` to leave it. In an editor, select
`.venv/bin/python` as the Python interpreter.

## Installed tools

| Packages | Purpose |
| --- | --- |
| `openai`, `google-genai`, `anthropic` | Official SDKs for OpenAI, Gemini, and Claude |
| `httpx` | PubMed/OpenAlex HTTP requests and downloads |
| `pydantic` | Activity-schema validation and JSON Schema generation |
| `python-dotenv` | Load local configuration from `.env` in future scripts |
| `pypdf` | Extract embedded PDF text and page references |
| `pandas` | Organize and export literature and activity catalogs |
| `rapidfuzz` | Find candidate duplicate titles and activity descriptions |
| `tenacity`, `tqdm` | Configurable retries and progress reporting |

String similarity only identifies potential duplicates; it does not establish
semantic equivalence. PDF text extraction does not provide OCR or the section
and citation structure of GROBID. Add those services when the document-processing
milestone requires them. Simulation tools are also deferred until task selection.

## Configure a provider later

```sh
cp .env.example .env
```

Enter the API key for your selected provider in `.env`. The example contains
empty placeholders. `.env` is ignored by Git. Future scripts should explicitly
call `dotenv.load_dotenv()` before constructing an SDK client.

Provider documentation:

- [OpenAI Python SDK](https://developers.openai.com/api/reference/python)
- [Gemini Python SDK](https://ai.google.dev/gemini-api/docs/libraries)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)

This setup does not select a model or make model API calls.

## Reproduce or update dependencies

`requirements.in` lists the direct dependencies. `requirements.txt` records the
exact installed versions, including their dependencies, for this environment.
Use Python 3.13 to recreate it:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
```

To intentionally update dependencies, install from `requirements.in`, verify
the environment, and regenerate the version snapshot:

```sh
python -m pip install --upgrade -r requirements.in
python -m pip check
python -m pip freeze > requirements.txt
```
