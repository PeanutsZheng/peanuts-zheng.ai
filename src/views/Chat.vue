<template>
<div class='Chat'>
    <transition name="slide-fade" appear>
        <div class="chat-container">
            <div class="chat-history" ref="chatHistoryRef">
                <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
                    <div class="role">{{ message.role }}</div>
                    <div v-if="!message.isTyping" class="message-content">
                        {{ message.content }}
                    </div>
                    <div v-else class="message-content typing">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>

            <div class="chat-input-area">
                <textarea id="messageInput" v-model="messageInput"
                    placeholder="Input message..."
                    rows="3" @keydown="handleKeydown">
                </textarea>
                <button id="sendButton" @click="sendMessage">Send</button>
            </div>
        </div>
    </transition>

    <CtrlPanel ref="ctrlPanelRef" :widgets="widgets"/>

    <Popup ref="popupRef"/>
</div>
</template>

<script setup name='Chat' lang='ts'>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'
import { type IMessage, type IChat, type IChatValues } from '../types/chat'
import CtrlPanel from '../components/CtrlPanel.vue'
import { useChatCtrlPanelWidgets } from '../store/chatCtrlPanelWidgets'
import { useCtrlPanel } from '../hooks/useCtrlPanel'
import Popup from '../components/Popup.vue'
import { usePopup } from '../hooks/usePopup'

const widgets = useChatCtrlPanelWidgets()
const chatHistoryRef = ref<HTMLElement>()
const messageInput = ref('')
const messages = ref<IMessage[]>([])

const { ctrlPanelRef, registerCtrlPanelEvent,
    getCtrlPanelValues, setCtrlPanelValue } = useCtrlPanel()
const { popupRef, messagePopup } = usePopup()

const state = reactive({
    model: 'AI',
    chatHistory: [] as IChat[],
})

onMounted(() => {
    addMessageToChatHistory(
        state.model,
        'Hello, this is PeanutsZheng\'s ai, please chose an AI model first.',
        'received'
    )

    // Register widgets event
    registerCtrlPanelEvent('Model', 'onChange', () => { loadModel() })
    registerCtrlPanelEvent('Clear', 'onClick', () => { clearChatHistory() })
    registerCtrlPanelEvent('Unload', 'onClick', () => { unloadModel() })
})

// ==== FUNCTIONS ==== //
async function sendMessage() {
    let message = messageInput.value.trim()
    messageInput.value = ''

    if (!message)
        return

    if (state.model === 'AI') {
        messagePopup('Please select a model first.')
        return
    }

    addMessageToChatHistory('You', message, 'sent')

    // Add typing indicator
    const typingIndex = messages.value.length
    addMessageToChatHistory(state.model, '', 'received', true)

    const values = getCtrlPanelValues() as IChatValues
    let prompt = buildPromptWithHistory(message)

    const config = {
        'maxTokens': values['Max tokens'],
        'temperature': values['temperature'],
        'topP': values['top-p'],
    }
    try {
        const response = await axios.post(`${values['API Key']}/generate`, {
            prompt: prompt,
            config: config
        })

        const result = await response.data
        // Remove typing indicator
        messages.value = messages.value.filter((_, i) => i !== typingIndex)
        
        let modelResponse = result.response
        if (!modelResponse || modelResponse.length === 0)
            throw new Error('No response from model.')

        addMessageToChatHistory(state.model, modelResponse, 'received')

        addTochatHistory({ role: "user", content: message })
        addTochatHistory({ role: "assistant", content: modelResponse })
    } catch (error) {
        // Remove typing indicator
        messages.value = messages.value.filter((_, i) => i !== typingIndex)
        messagePopup(`Generate error: ${error}`, 3000)
    }
}

async function loadModel() { 
    if (state.model !== 'AI') {
        if (!await unloadModel())
            return messagePopup(`Failed to unload model ${state.model}.`, 3000);
    }

    const values = getCtrlPanelValues() as IChatValues
    const selectModel = values['Model']

    if (!selectModel || selectModel === state.model)
        return

    messagePopup(`Loading model ${selectModel} ...`)
    try {
        const response = await axios.post(`${values['API Key']}/load-model`, {
            model: selectModel
        })

        const result = await response.data
        if (result.success) {
            clearChatHistory()
            state.model = selectModel
            // Set system prompt
            const systemPrompt = ''
            setCtrlPanelValue('System prompt', systemPrompt)
            messagePopup(`Load ${selectModel}: ${result.message}.`)
        }
        else 
            messagePopup(`Failed to load ${selectModel}: ${result.message}`, 3000)
    } catch (error) {
        messagePopup(`Loading ${selectModel} error: ${error}`, 3000)
    }
}

async function unloadModel() { 
    const values = getCtrlPanelValues() as IChatValues
    messagePopup(`Unloading ${state.model} ...`)
    try {
        const response = await axios.post(`${values['API Key']}/unload-model`)

        const result = await response.data
        if (!result.success) {
            messagePopup(`Failed to unload ${state.model}: ${result.message}`, 3000)
            return false
        }

        messagePopup(`Unload ${state.model}: ${result.message}`);
        state.model = 'AI';
        setCtrlPanelValue('System prompt', '')
        clearChatHistory()    
        return true
    } catch (error) {
        messagePopup(`Unload ${state.model} error: ${error}`, 3000)
        return false
    }
}

function addTochatHistory(chat: IChat) {
    state.chatHistory.push(chat)

    if (state.chatHistory.length > 10)
        state.chatHistory.shift()
}

function buildPromptWithHistory(currentMessage: string) {
    const values = getCtrlPanelValues() as IChatValues
    let systemPrompt = values['System prompt']
    let prompt = [{ role: 'system', content: systemPrompt }]
    prompt = prompt.concat(state.chatHistory)
    prompt.push({ role: "user", content: currentMessage })

    return prompt
}

function addMessageToChatHistory(
    role: string,
    content: string,
    type: 'sent' | 'received',
    isTyping: boolean = false)
{
    messages.value.push({role, content, type, isTyping })
    
    // Roll to bottom
    setTimeout(() => {
        if (chatHistoryRef.value)
            chatHistoryRef.value.scrollTop = chatHistoryRef.value.scrollHeight
    }, 0)
}

function clearChatHistory() {
    state.chatHistory = []
    messages.value = []
}

function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault()
        sendMessage()
    }
}
</script>

<style scoped>
/* Slide in / out */
.slide-fade-enter-active {
    transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
    transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from {
    transform: translateX(20px);
    opacity: 0;
}

.slide-fade-leave-to {
    transform: translateX(-20px);
    opacity: 0;
}

* {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
</style>