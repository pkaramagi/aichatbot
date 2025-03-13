export interface ChatMessage {
    id: string;
    text: string;
    sender: 'user' | 'system';
    timestamp: Date;
}
