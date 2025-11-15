import { ref, type Ref } from 'vue'
import Popup from '../components/Popup.vue'

interface UsePopupReturn {
    popupRef: Ref<InstanceType<typeof Popup> | undefined>
    messagePopup: (message: string, duration?: number) => void
}

export function usePopup(): UsePopupReturn {
    const popupRef = ref<InstanceType<typeof Popup> | undefined>(undefined)

    function messagePopup(message: string, duration: number = 2000) {
        popupRef.value?.popup(message, duration)
    }

    return {
        popupRef,
        messagePopup
    }
}