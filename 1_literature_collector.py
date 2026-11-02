
import numpy as np
import httpx
import xml.etree.ElementTree as ET
import time
import json
from datetime import datetime, timezone
from uuid import uuid4
from queries import QUERIES_EXP2
from csv_export import export_json_to_csv


# Output settings
EXPORT_CSV = True  # Set to False to save JSON only.


url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
url_fetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def get_params_broad_query(query):
    "establish parameters of the queries"
    params = {
    "db": "pubmed",
    "term": query.strip(),
    "retmode": "json",
    "retmax": 10,
    "sort": "relevance",
    }
    return params

def get_params_ind_paper(paper_id):
    "establish parameters of one paper"
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "xml"
            }
    return params

def get_element_text(element):
    "Return complete text, including nested formatting, or None if missing."
    if element is None:
        return None
    return "".join(element.itertext()).strip() or None


def log_search(query_number, params, payload, run_id, searched_at):
    """Append one search response to the log and return its unique ID."""
    result = payload.get("esearchresult", {})
    errors = payload.get("error") or result.get("errorlist")
    if "esearchresult" not in payload and not errors:
        errors = "PubMed did not return an esearchresult."

    search_id = str(uuid4())
    total_matches = result.get("count")
    returned_pmids = result.get("idlist", [])
    entry = {
        "RunID": run_id,
        "SearchID": search_id,
        "QueryNumber": query_number,
        "Database": params["db"],
        "QueryText": params["term"],
        "SearchDate": searched_at,
        "SearchStatus": "error" if errors else "ok",
        "TotalMatches": int(total_matches) if total_matches is not None else None,
        "ReturnedCount": len(returned_pmids),
        "ReturnedPMIDs": returned_pmids,
        "Sort": params.get("sort"),
        "RetMax": params.get("retmax"),
        "RetStart": params.get("retstart", 0),
        "QueryTranslation": result.get("querytranslation"),
        "Warnings": result.get("warninglist") or {},
        "Errors": errors or {},
    }
    # JSON Lines keeps previous runs: one complete JSON object per line.
    with open("search_log.jsonl", "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return search_id


def remove_duplicates(papers):
    """Keep the first record per PMID and collect all queries and SearchIDs.

    This helper can clean previously saved data. The retrieval loop below
    checks for duplicates before downloading each paper.
    QueryNumber remains the first record's original query. Records without a
    PMID remain separate. The input records are not modified.
    """
    unique_papers = []
    papers_by_pmid = {}

    for paper in papers:
        pmid = paper.get("PMID")
        pmid = str(pmid).strip() if pmid is not None else ""

        if pmid and pmid in papers_by_pmid:
            kept_paper = papers_by_pmid[pmid]
        else:
            kept_paper = dict(paper)
            kept_paper["QueryNumbers"] = []
            kept_paper["SearchIDs"] = []
            unique_papers.append(kept_paper)
            if pmid:
                papers_by_pmid[pmid] = kept_paper

        query_numbers = list(paper.get("QueryNumbers") or [])
        if paper.get("QueryNumber") is not None:
            query_numbers.append(paper["QueryNumber"])
        for query_number in query_numbers:
            if query_number not in kept_paper["QueryNumbers"]:
                kept_paper["QueryNumbers"].append(query_number)
        for search_id in paper.get("SearchIDs") or []:
            if search_id not in kept_paper["SearchIDs"]:
                kept_paper["SearchIDs"].append(search_id)

    return unique_papers


query_number = 1 #count to keep track of which query we are looking at
run_id = str(uuid4())

query_list = QUERIES_EXP2
final = []
papers_by_pmid = {}
for query in query_list:
    print('Query Number:', query_number)

    #go through each query and get the top 10 results

    params = get_params_broad_query(query)
    time.sleep(1)
    searched_at = datetime.now(timezone.utc).isoformat()
    response = httpx.get(url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    result = payload.get("esearchresult", {})
    search_id = log_search(query_number, params, payload, run_id, searched_at)
    if payload.get("error") or result.get("errorlist") or "esearchresult" not in payload:
        raise RuntimeError("PubMed search returned an error; see search_log.jsonl.")

    #For each paper get key information
    for id in result["idlist"]:
        paper_id = str(id).strip()
        existing_paper = papers_by_pmid.get(paper_id)
        if existing_paper is not None:
            # Reuse the record, but retain every search that found it.
            if query_number not in existing_paper["QueryNumbers"]:
                existing_paper["QueryNumbers"].append(query_number)
            if search_id not in existing_paper["SearchIDs"]:
                existing_paper["SearchIDs"].append(search_id)
            continue

        param_paper = get_params_ind_paper(paper_id)
        time.sleep(1)
        single_paper = httpx.get(url_fetch, params=param_paper, timeout=30)
        single_paper.raise_for_status()
        # Parse the XML content
        root = ET.fromstring(single_paper.content)

        # PubMed returns journal articles and book chapters in different layouts.
        record = root.find("PubmedArticle")
        citation_path = "MedlineCitation"
        document_path = "MedlineCitation/Article"
        metadata_path = "PubmedData"
        date_path = "Journal/JournalIssue/PubDate"
        if record is None:
            record = root.find("PubmedBookArticle")
            citation_path = "BookDocument"
            document_path = "BookDocument"
            metadata_path = "PubmedBookData"
            date_path = "Book/PubDate"
        if record is None:
            raise ValueError(f"No supported PubMed record returned for PMID {paper_id}.")
        document = record.find(document_path)
        if document is None:
            raise ValueError(f"Missing document metadata for PMID {paper_id}.")

        #for each paper, loop and get relevant information
        fields = {
            "PMID": f"{citation_path}/PMID",
            "Title": f"{document_path}/ArticleTitle",
            "JournalTitle": f"{document_path}/Journal/Title",
            "BookTitle": f"{document_path}/Book/BookTitle",
            "doi": f"{metadata_path}/ArticleIdList/ArticleId[@IdType='doi']",
            "pmc": f"{metadata_path}/ArticleIdList/ArticleId[@IdType='pmc']",
        }

        paper_info = {"RecordType": record.tag}

        for name, path in fields.items():
            element = record.find(path)
            paper_info[name] = get_element_text(element)

        if paper_info["PMID"] != paper_id:
            raise ValueError(
                f"Requested PMID {paper_id}, but the fetched record has "
                f"PMID {paper_info['PMID']!r}."
            )

        # Abstracts can have multiple labeled sections.
        paper_info["Abstract"] = []
        for section in document.findall("Abstract/AbstractText"):
            paper_info["Abstract"].append({
                "label": section.get("Label"),
                "text": get_element_text(section),
            })

        # Read names only, so affiliations are not mixed into author names.
        paper_info["Authors"] = []
        for author in document.findall("AuthorList/Author"):
            collective_name = get_element_text(author.find("CollectiveName"))
            if collective_name:
                author_name = collective_name
            else:
                given_name = (
                    get_element_text(author.find("ForeName"))
                    or get_element_text(author.find("Initials"))
                )
                last_name = get_element_text(author.find("LastName"))
                suffix = get_element_text(author.find("Suffix"))
                author_name = " ".join(
                    part for part in (given_name, last_name, suffix) if part
                ) or None
            paper_info["Authors"].append(author_name)

        # These fields can also occur more than once.
        paper_info["Language"] = [
            get_element_text(element)
            for element in document.findall("Language")
        ]
        paper_info["PublicationType"] = [
            get_element_text(element)
            for element in (
                document.findall("PublicationTypeList/PublicationType")
                + document.findall("PublicationType")
            )
        ]

        # Preserve partial publication dates without inventing missing parts.
        pub_date = document.find(date_path)
        date_fields = {
            "year": "Year",
            "month": "Month",
            "day": "Day",
            "season": "Season",
            "medline_date": "MedlineDate",
        }
        paper_info["PubDate"] = {}
        paper_info["QueryNumber"] = query_number
        paper_info["QueryNumbers"] = [query_number]
        paper_info["SearchIDs"] = [search_id]
        for name, tag in date_fields.items():
            element = pub_date.find(tag) if pub_date is not None else None
            paper_info["PubDate"][name] = get_element_text(element)

        final.append(paper_info)
        papers_by_pmid[paper_id] = paper_info
        #store information on an excel sheet
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=4)
    if EXPORT_CSV:
        export_json_to_csv("output.json", "output.csv")

    query_number +=1









