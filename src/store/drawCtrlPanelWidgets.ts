import { ref } from 'vue'
import { type IWidget } from '../types/widgets'

const ctrlPanelWidgets: IWidget[] = [
    {
        label: 'API Key',
        component: 'input',
        props: {
            type: 'text',
            value: 'http://localhost:5001/api',
        }
    },
    {
        label: 'Strength',
        component: 'input',
        props: {
            type: 'range',
            min: '0',
            max: '1',
            value: '0.8',
            step: '0.01'
        }
    },
    {
        label: 'do cfg',
        component: 'input',
        props: {
            type: 'checkbox',
            checked: 'true'
        }
    },
    {
        label: 'cfg scale',
        component: 'input',
        props: {
            type: 'range',
            min: '0',
            max: '14',
            value: '7.5',
            step: '0.1'
        }
    },
    {
        label: 'Sampler',
        component: 'input',
        props: {
            type: 'text',
            value: 'ddpm'
        }
    },
    {
        label: 'Steps',
        component: 'input',
        props: {
            type: 'number',
            value: '50',
        }
    },
    {
        label: 'Seed',
        component: 'input',
        props: {
            type: 'number',
            value: '42'
        }
    }
]

export function useDrawCtrlPanelWidgets() {
    return ref(ctrlPanelWidgets)
}