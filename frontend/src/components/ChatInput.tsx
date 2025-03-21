import { useState } from "react";

interface ChatInputProps {
   onSend: (message:string) => void;
}


function ChatInput({onSend}:ChatInputProps){
    const [message, setMessage] = useState('');
    const handleSubmit = (e:React.FormEvent) =>{
        e.preventDefault();
        const trimmedMessage = message.trim();
        if(trimmedMessage){
            onSend(message);
            setMessage('');
        }
    };

    return (
        <form onSubmit = {handleSubmit} className="flex gap-2 p-4 bg-gray-100">
            <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type a message..."
                className="flex-1 p-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500"
            />
            <button type="submit" disabled={!message.trim()} className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600">Send</button>
        </form>
    );

};

export default ChatInput;