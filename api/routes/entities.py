from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from common.entities import Entities
import logging
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/",response_class=JSONResponse)
async def get_entities():
    ent = Entities()
    
    return ent.get_nodes()

@router.get("/{entity}",response_class=JSONResponse)
async def get_entity(entity: str):
    try:
        ent = Entities(entity_name=entity)
        
        return {"nodes": ent.get_nodes(),
                "edges": ent.get_edges()
                }
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
## Add response model

@router.get("/relations/{entity}",response_class=JSONResponse)
async def get_entity_relations(entity: str):
    try:
        ent = Entities(entity_name=entity)
        return ent.get_entity_relations()
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/relations/{entity}/filtered",response_class=JSONResponse)
async def get_entity_relations_filtered(entity: str):
    try:
        ent = Entities(entity_name=entity)
        return ent.get_entity_relations_filtered()
    
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
## Add response model
