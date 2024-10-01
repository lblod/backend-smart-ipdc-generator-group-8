from config import TIKA_ENDPOINT
from schemas import DecisionProcessingRequest, DecisionDatabaseQueryResponse, IPDCEntrySave, ProcessingResponse, IPDCEntry, RetrieveResponse
from fastapi import Request
from helpers import query
from typing import Any
import requests
import tempfile
from escape_helpers import sparql_escape_uri


def retrieve_raw_decision(uri: str, request: Request) -> DecisionDatabaseQueryResponse:
    the_query = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX meb: <http://rdf.myexperiment.org/ontologies/base/>
        PREFIX adms: <http://www.w3.org/ns/adms#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX mu: <http://mu.semte.ch/vocabularies/core/>
        PREFIX pav: <http://purl.org/pav/>
        PREFIX ext: <http://mu.semte.ch/vocabularies/ext/>
        SELECT DISTINCT ?besluit ?besluitType ?bestuurseenheid (group_concat(distinct ?file;separator=",") as ?files)  WHERE {{
          <{0}> a meb:Submission;
                      pav:createdBy ?bestuurseenheid;
                        adms:status ?status;
                      dct:subject ?besluit;
                       prov:generated ?formData.
          ?formData dcterms:hasPart ?remoteUrl;
                    ext:decisionType ?besluitType.
          ?remoteUrl mu:uuid ?uuid.
          BIND(CONCAT("https://besluit-meldingen.source-hackathon-ai-wave-2.s.redhost.be", "/files/", ?uuid, "/download") as ?file)
        }}
    """.format(uri)
    results = query(the_query, request)
    return DecisionDatabaseQueryResponse(**results)


def process_raw_decision_to_raw_content(decision_raw: DecisionDatabaseQueryResponse) -> str:
    content = []
    for bind in decision_raw.results.bindings:
        url = bind.files.value
        r = requests.get(url, allow_redirects=True)
        tika_response = requests.put(TIKA_ENDPOINT, r.content, headers={
            'Accept': 'text/plain'});
        content.append(str(tika_response.content))
    return " ".join(content)


def ai_parse(raw_content: str, uri: str) -> IPDCEntry:
    """ Here we call the AI service, dummy for now """
    return IPDCEntry(
        description="test",
        besluitendatabank_uri=uri,
        name="test"
    )


@app.get("/hello")
async def hello():
    return {"message": "Hello from mu-python-ml!"}


@app.post("/decision")
async def request_processing(
    body: DecisionProcessingRequest,
    request: Request
) -> ProcessingResponse:
    decision_raw = retrieve_raw_decision(body.uri, request)
    raw_content = process_raw_decision_to_raw_content(decision_raw)
    ipdc_entry = ai_parse(raw_content)
    return ProcessingResponse(
        entry=ipdc_entry,
        raw_content=raw_content
    )

