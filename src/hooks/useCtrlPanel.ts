import { ref, type Ref } from 'vue'
import CtrlPanel from '../components/CtrlPanel.vue'
import { type IChatValues } from '../types/chat'
import { type IDrawValues } from '../types/draw'

interface UseCtrlPanelReturn {
    ctrlPanelRef: Ref<InstanceType<typeof CtrlPanel> | undefined>

    registerCtrlPanelEvent: (label: string, eventName: string, handler: Function) => void
    getCtrlPanelValues: () => IChatValues | IDrawValues | undefined
    setCtrlPanelValue: (label: string, value: any) => void
}

export function useCtrlPanel(): UseCtrlPanelReturn {
    const ctrlPanelRef = ref<InstanceType<typeof CtrlPanel>>()

    const registerCtrlPanelEvent = (label: string, eventName: string, handler: Function) => {
        ctrlPanelRef.value?.registerEventHandler(label, eventName, handler)
    }

    const getCtrlPanelValues = (): IChatValues | IDrawValues | undefined => {
        return ctrlPanelRef.value?.getValues() as IChatValues | undefined
    }

    const setCtrlPanelValue = (label: string, value: any) => {
        ctrlPanelRef.value?.setValue(label, value)
    }

    return {
        ctrlPanelRef,
        registerCtrlPanelEvent,
        getCtrlPanelValues,
        setCtrlPanelValue
    };
}