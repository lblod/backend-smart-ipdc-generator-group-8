from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


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


class IPDCBaseType(BaseModel):
    description: str
    name: Optional[str]


class IPDCProcedure(IPDCBaseType):
    pass


class IPDCCost(IPDCBaseType):
    pass


class IPDCProof(BaseModel):
    description: str
    name: Optional[str]


class IPDCCondition(IPDCBaseType):
    proof: Optional[IPDCProof]


class IPDCRegulation(IPDCBaseType):
    url: Optional[str]


class IPDCFinancialAdvantage(IPDCBaseType):
    pass


class ThemaCategories(Enum):
    BOUWEN_EN_WONEN="Bouwen en Wonen"
    BURGER_EN_OVERHEID="Burger en Overheid"
    CULTUUR_SPORT_EN_VRIJE_TIJD="Cultuur, Sport en Vrije Tijd"
    ECONOMIE_EN_WERK="Economie en Werk"
    MILIEU_EN_ENERGIE="Milieu en Energie"
    MOBILITEIT_EN_OPENBARE_WERKEN="Mobiliteit en Openbare Werken"
    ONDERWIJS_EN_WETENSCHAP="Onderwijs en Wetenschap"
    WELZIJN_EN_GEZONDHEID="Welzijn en Gezondheid"


class TypeCategories(Enum):
    ADVIES_EN_BEGELEIDING="Advies en begeleiding"
    BEWIJS="Bewijs"
    FINANCIEEL_VOORDEEL="Financieel voordeel"
    FINANCIELE_VEPLICHTING="Financiële verplichting"
    INFRASTRUCTUUR_EN_MATERIAAL="Infrastructuur en materiaal"
    TOELATING="Toelating"
    VOORWERP="Voorwerp"


class DoelgroepCategories(Enum):
    ANDERE_ORGANISATIE="Andere organisatie"
    BURGER="Burger"
    LOKAAL_BESTUUR="Lokaal bestuur"
    ONDERNEMING="Onderneming"
    VERENIGING="Vereniging"
    VLAAMSE_OVERHEID="Vlaamse overheid"


class BevoegdBestuursniveauCategories(Enum):
    EUROPESE_OVERHEID="Europese Overheid"
    FEDERALE_OVERHEID="Federale Overheid"
    LOKALE_OVERHEID="Lokale Overheid"
    PROVENCIALE_OVERHEID="Provinciale Overheid"
    VLAAMSE_OVERHEID="Vlaamse Overheid"


class UitvoerendBestuursniveauCategories(Enum):
    DERDEN="Derden"
    EUROPESE_OVERHEID="Europese Overheid"
    FEDERALE_OVERHEID="Federale Overheid"
    LOKALE_OVERHEID="Lokale Overheid"
    PROVENCIALE_OVERHEID="Provinciale Overheid"
    VLAAMSE_OVERHEID="Vlaamse Overheid"


class IPDCEntry(BaseModel):
    description: str
    besluitendatabank_uri: str
    name: str
    procedure: List[IPDCProcedure] = []
    cost: List[IPDCCost] = []
    condition: List[IPDCCondition] = []
    entry_theme: List[ThemaCategories] = []
    entry_type: Optional[TypeCategories] = None
    entry_doelgroep: List[DoelgroepCategories] = []
    bevoegde_overheden: List[str] = []
    uitvoerende_overheden: List[str] = []
    bevoegde_bestuursniveau: List[BevoegdBestuursniveauCategories] = []
    uitvoerende_bestuursniveau: List[UitvoerendBestuursniveauCategories] = []


class ProcessingResponse(BaseModel):
    entry: IPDCEntry
    raw_content: str


class RetrieveResponse(BaseModel):
    raw_content: str