import { ChatMessage as ChatMessageType } from "../types"
import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
interface ChatWindowProps {
    messages: ChatMessageType[];
    onSend: (message:string) => void;
}

function ChatWindow({messages, onSend}:ChatWindowProps){
    return (
        <div className="flex flex-col h-screen bg-white">
            <div className ="flex-1 p-4 overflow-y-auto">
                {messages.map((message)=>(
                    <ChatMessage key={message.id} message={message}/>   
                ))}
            </div>
            <ChatInput onSend={onSend}/>
        </div>
    )

}

export default ChatWindow;