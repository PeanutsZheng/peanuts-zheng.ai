export interface IChat {
    role: string,
    content: string
}

export interface IMessage extends IChat {
    type: 'sent' | 'received',
    isTyping?: boolean
}

export interface IChatValues {
    'API Key': string,
    'Max tokens': number,
    'Model': string,
    'System prompt': string,
    'temperature': number,
    'top-p': number,
}