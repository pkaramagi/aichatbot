import { ChatMessage as ChatMessageType } from '../types'  

interface ChatMessageProps {
    message: ChatMessageType;
}

function ChatMessage({message}:ChatMessageProps){
    return (
        <div className ={`flex ${message.sender === 'user'? 'justify-end': 'justify-start'} mb-4`}>
            <div className={`rounded-lg p-3 max-w-[70%] ${message.sender === 'user'? 'bg-blue-500 text-white': 'bg-gray-200 text-gray-800'}`}>
                <p>{message.text}</p>
                <span className="text-xs text-gray-500">
                    {message.timestamp.toLocaleTimeString()}
                </span>
            </div>
        </div>
    );
}

export default ChatMessage;