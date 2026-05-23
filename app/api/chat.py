from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import process_message
from app.models.database import SessionLocal
from app.models.chat import Conversation

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    intent: str
    reply: str


@router.post("", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")

    result = process_message(req.message, req.session_id)

    # Persist to DB
    db = SessionLocal()
    try:
        db.add(Conversation(
            session_id=result["session_id"],
            role="user",
            content=req.message,
            intent=result["intent"],
        ))
        db.add(Conversation(
            session_id=result["session_id"],
            role="assistant",
            content=result["reply"],
            intent=result["intent"],
        ))
        db.commit()
    finally:
        db.close()

    return ChatResponse(**result)


@router.get("/history/{session_id}")
def get_history(session_id: str):
    db = SessionLocal()
    try:
        records = (
            db.query(Conversation)
            .filter(Conversation.session_id == session_id)
            .order_by(Conversation.created_at.asc())
            .all()
        )
        return [
            {
                "role": r.role,
                "content": r.content,
                "intent": r.intent,
                "time": r.created_at.isoformat() if r.created_at else None,
            }
            for r in records
        ]
    finally:
        db.close()
