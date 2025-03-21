import { useState } from "react";
import { ChatMessage } from "../types";

function useChat(){
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    
    const sendMessage = async(message:string) =>{
        
        const userMessage: ChatMessage = {
            id: Date.now().toString(),
            text: message,
            sender: 'user',
            timestamp: new Date(),
        }

      

        setMessages((prev)=> [...prev, userMessage])

        try {
            const response = await fetch('http://localhost:8000/api/v1/chat/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({question: message})
            });
        
            if (response.ok) {
                // Create the system message first
                const systemMessage: ChatMessage = {
                    id: Date.now().toString(),
                    text: '',
                    sender: 'system',
                    timestamp: new Date(),
                };
        
                setMessages((prev) => [...prev, systemMessage]);
        
                
                const reader = response.body?.getReader();
                if (!reader) {
                    throw new Error('No reader available');
                }
        
               
                const textDecoder = new TextDecoder();
                let currentText = '';
        
                while (true) {
                    const { done, value } = await reader.read();
                    if (done) {
                        break;
                    }
        
                    
                    const chunk = textDecoder.decode(value, { stream: true });
        
                    
                    currentText += chunk;
        
                   
                    setMessages((prev) =>
                        prev.map((message) =>
                            message.id === systemMessage.id
                                ? { ...message, text: currentText }
                                : message
                        )
                    );
                }
            } else {
                throw new Error('Failed to fetch response');
            }
        } catch (error) {
            console.error('Error sending message:', error);
        }
        
    };
    return {messages, sendMessage};
};

export default useChat;