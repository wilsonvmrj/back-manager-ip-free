from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from back.database import get_session
from back.schemas import VlanList, VlanPublic, VlanSchema
from back.models import User, Vlan

from sqlalchemy import select

from sqlalchemy.orm import Session

from back.security import get_current_user


router = APIRouter(prefix='/vlans',tags=['vlans'])

T_Session = Annotated[Session,Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED,response_model=VlanPublic)
def create_vlan(
    vlan: VlanSchema,
    session: T_Session,
    user: T_CurrentUser 
    ):

    db_vlan = session.scalar(
        select(Vlan).where(
            (Vlan.vlan == vlan.vlan)
        )
    )
    if db_vlan:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Vlan already exists',
        )
    
    db_vlan = Vlan(
        vlan=vlan.vlan,
        network=vlan.network,
        netmask=vlan.netmask,
        gateway=vlan.gateway,
        description=vlan.description,
    )

    session.add(db_vlan)
    session.commit()
    session.refresh(db_vlan)

    return db_vlan

    
@router.get('/',response_model=VlanList)
def read_vlans(
    
    session: T_Session,
    user: T_CurrentUser,
    limit: int = 10,
    offset: int =0,
):
    vlans = session.scalars(select(Vlan).limit(limit).offset(offset))
    return {'vlans': vlans}
    
