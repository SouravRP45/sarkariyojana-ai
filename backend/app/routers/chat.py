from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime
import json
import logging
from app.models import ChatRequest, ChatResponse, UserProfile
from app.services.rag_engine import rag_engine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("", response_model=ChatResponse)
async def chat_rest(request: ChatRequest):
    """REST endpoint for chat queries."""
    response_text = rag_engine.generate_response(
        user_query=request.message,
        user_profile=request.user_profile,
        chat_history=request.chat_history
    )
    
    return ChatResponse(
        content=response_text,
        timestamp=datetime.now().isoformat()
    )

@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time chat."""
    await websocket.accept()
    chat_history = []
    user_profile = None

    try:
        while True:
            data_str = await websocket.receive_text()
            try:
                data = json.loads(data_str)
                user_message = data.get("message", "")
                
                # Update profile if provided in the message payload
                profile_dict = data.get("user_profile")
                if profile_dict:
                     user_profile = UserProfile(**profile_dict)

                if not user_message:
                    continue

                chat_history.append({"role": "user", "content": user_message})

                # Acknowledge receipt/typing indicator logic can go here
                
                response_text = rag_engine.generate_response(
                    user_query=user_message,
                    user_profile=user_profile,
                    chat_history=chat_history
                )
                
                chat_history.append({"role": "assistant", "content": response_text})

                response = ChatResponse(
                    content=response_text,
                    timestamp=datetime.now().isoformat()
                )
                
                await websocket.send_json(response.model_dump())

            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON format"})
            except Exception as e:
                logger.error(f"Error processing WS message: {e}")
                await websocket.send_json({"error": "Internal server error processing message"})

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
