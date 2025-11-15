import { ref } from 'vue'
import { type IWidget } from '../types/widgets'

const ctrlPanelWidgets: IWidget[] = [
    {
        label: 'API Key',
        component: 'input',
        props: {
            type: 'text',
            value: 'http://localhost:5000/api',
        }
    },
    {
        label: 'Model',
        component: 'select',
        props: {
            options: [
                { value: '', label: '/' },
                { value: 'Llama-3.2-3B-Instruct', label: 'Llama-3.2-3B-Instruct' }
            ],
        }
    },
    {
        label: 'Max tokens',
        component: 'input',
        props: {
            type: 'range',
            min: 0,
            max: 1024,
            value: 256,
            step: 1
        }
    },
    {
        label: 'temperature',
        component: 'input',
        props: {
            type: 'range',
            min: 0,
            max: 1,
            value: 0.6,
            step: 0.01
        }
    },
    {
        label: 'top-p',
        component: 'input',
        props: {
            type: 'range',
            min: 0,
            max: 1,
            value: 0.9,
            step: 0.01
        }
    },
    {
        label: 'System prompt',
        component: 'textarea',
        props: {
            value: "You are a chatbot that answers questions about the world.",
            rows: 4
        }
    },
    {
        label: 'Clear',
        component: 'button',
        props: { innerText: 'Clear' }
    },
    {
        label: 'Unload',
        component: 'button',
        props: { innerText: 'Unload' }
    }
]

export function useChatCtrlPanelWidgets() {
    return ref(ctrlPanelWidgets)
}