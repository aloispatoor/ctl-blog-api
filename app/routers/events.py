from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.db import get_session
from app.models.event import EventPublic, EventCreate, Event, EventUpdate

router = APIRouter()

# CREATE EVENT
@router.post(
    "/events/",
    response_model=EventPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create an event",
    response_description="The created event",
)
async def create_event(event_create: EventCreate, session: Session = Depends(get_session)):
    event = Event.model_validate(event_create)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

# GET ALL EVENTS
@router.get(
    "/events/",
    response_model=list[EventPublic],
    summary="Get all events",
    response_description="The list of events",
)
async def get_events(session: Session = Depends(get_session)):
    events = session.exec(select(Event)).all()
    return events

# GET ONE EVENT
@router.get(
    "/events/{id}",
    response_model=EventPublic,
    summary="Get an event",
    response_description="The one event",
)
async def get_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

# UPDATE EVENT
@router.patch(
    "/events/{id}",
    response_model=EventPublic,
    summary="Update an event",
    response_description="The updated event",
)
async def update_event(event_id: int, event_update: EventUpdate, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event_data = event_update.model_dump(exclude_unset=True)
    event.sqlmodel_update(event_data)
    session.add(event)
    session.commit()
    session.refresh(event)
    return event

# DELETE AN EVENT
@router.delete(
    "/events/{id}",
    response_model=EventPublic,
    summary="Delete an event",
    response_description="The deleted event",
)
async def delete_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    session.delete(event)
    session.commit()
    return event