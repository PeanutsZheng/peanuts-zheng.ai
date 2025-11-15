<template>
  <div id="messagePopupContainer" class="popup-container">
    <div v-for="item in messages" :key="item.id"
        class="popup-message-item" :class="{ show: item.visible }">
        <span class="popup-close" @click="removeMessage(item.id)">&times;</span>
        <div class="popup-message-text">{{ item.message }}</div>
        </div>
    </div>
</template>

<script setup name="Popup" lang="ts">
import { ref, onMounted } from 'vue'
import { type IPopup } from '../types/popup'

const messages = ref<IPopup[]>([])

function popup(message: string, duration: number = 2000) {
    const id = Date.now()
    
    // 3 messages limit
    if (messages.value.length > 3) {
        const lastMessage = messages.value[messages.value.length - 1] || {} as IPopup
        removeMessage(lastMessage.id)
    }

    messages.value.unshift({ id, message, visible: false })

    setTimeout(() => {
        const msg = messages.value.find(m => m.id === id)
        if (msg) msg.visible = true
    }, 10)

    // Timeout close
    if (duration > 0) {
        setTimeout(() => { removeMessage(id)}, duration)
    }
}

function removeMessage(id: number) {
    const index = messages.value.findIndex(msg => msg.id === id)
    if (index === -1)
        return

    const message = messages.value[index]
    if (!message) 
        return

    message.visible = false
    setTimeout(() => {
        messages.value = messages.value.filter(msg => msg.id !== id)
    }, 300)
}

defineExpose({ popup })

onMounted(() => { (window as any).messagePopup = popup })
</script>

<style scoped>
</style>