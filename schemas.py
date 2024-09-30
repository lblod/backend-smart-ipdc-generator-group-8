from pydantic import BaseModel
from typing import List


class DecisionProcessingRequest(BaseModel):
    uri: str


class DecisionDatabaseQueryResultsBindingType(BaseModel):
    value: str
    type: str


class DecisionDatabaseQueryResultsBinding(BaseModel):
    files: DecisionDatabaseQueryResultsBindingType
    bestuurseenheid: DecisionDatabaseQueryResultsBindingType
    besluitType: DecisionDatabaseQueryResultsBindingType
    besluit: DecisionDatabaseQueryResultsBindingType


class DecisionDatabaseQueryResults(BaseModel):
    ordered: bool
    distinct: bool
    bindings: List[DecisionDatabaseQueryResultsBinding]


class DecisionDatabaseQueryHead(BaseModel):
    vars: List[str]
    link: List[str]


class DecisionDatabaseQueryResponse(BaseModel):
    results: DecisionDatabaseQueryResults
    head: DecisionDatabaseQueryHead


