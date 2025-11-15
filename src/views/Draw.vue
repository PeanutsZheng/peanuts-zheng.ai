<template>
<div class='Draw'>
    <transition name="slide-fade" appear>
        <div class="inputs">
            <div class="prompts-input-area">
                <label>Prompt</label>
                <textarea v-model="prompt" placeholder="Prompt" rows="1"></textarea>

                <label>Unconditional Prompt</label>
                <textarea v-model="uncond_prompt" placeholder="Unconditional prompt" rows="1"></textarea>

                <button id="generateBtn" @click="generate">Generate</button>
            </div>

            <div class="image-input-area">
                <label>Input Image</label>
                <div id="input_image" class="image" title="Upload an image" @click="triggerFileInput">
                    <input ref="fileInputRef" type="file" style="display: none;"
                        accept="*.png,*.jpg,*.jpeg" @change="handleFileSelect">
                    <img v-if="inputImage"  :src="inputImage">
                </div>
            </div>
        </div>
    </transition>

    <label>Output image</label>
    <transition name="slide-fade" appear>
        <div id="output_image" class="image" @click="showViewer">
            <img v-if="outputImage" :src="outputImage">
        </div>
    </transition>

    <CtrlPanel ref="ctrlPanelRef" :widgets="widgets"/>

    <Popup ref="popupRef"/>

    <!-- Large image viewer -->
    <div class="modal" v-if="showView" @click="closeViewer">
        <span class="close" @click="closeViewer">&times;</span>
        <img :src="outputImage" class="modal-content">
    </div>
</div>
</template>

<script setup name='Draw' lang='ts'>
import { ref } from 'vue';
import axios from 'axios';
import { type IDrawValues } from '../types/draw'
import CtrlPanel from '../components/CtrlPanel.vue';
import { useDrawCtrlPanelWidgets } from '../store/drawCtrlPanelWidgets';
import { useCtrlPanel } from '../hooks/useCtrlPanel'
import Popup from '../components/Popup.vue';
import { usePopup } from '../hooks/usePopup';

const widgets = useDrawCtrlPanelWidgets()
const fileInputRef = ref<HTMLInputElement>()
const prompt = ref('')
const uncond_prompt = ref('')
const inputImage = ref<string>()
const outputImage = ref<string>()
const showView = ref(false)

const { ctrlPanelRef, getCtrlPanelValues } = useCtrlPanel()
const { popupRef, messagePopup } = usePopup()

// ==== FUNCTIONS ==== //
async function generate() {
    if (!prompt.value)
        return

    const values = getCtrlPanelValues() as IDrawValues

    messagePopup('Loading models ...')
    try {
        const response = await axios.post(`${values['API Key']}/load-models`)
        const result = await response.data
        if (!result.success)
            return messagePopup('Failed to load models: ' + result.message)

        messagePopup(`Load models: ${result.message}`)
    }
    catch (error) {
        return messagePopup(`Load models error: ${error}`)
    }

    const formData = new FormData()
    formData.append('prompt', prompt.value)
    formData.append('uncond_prompt', uncond_prompt.value)
    if (inputImage.value)
        formData.append('input_image', inputImage.value)
    const config = {
        'cfg_scale': values['cfg scale'],
        'do_cfg': values['do cfg'],
        'sampler': values['Sampler'],
        'seed': values['Seed'],
        'steps': values['Steps'],
        'strength': values['Strength'],
    }
    formData.append('config', JSON.stringify(config))

    messagePopup('Generating ...')
    try {
        const response = await axios.post(`${values['API Key']}/generate`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        const result = await response.data

        if (!result.success)
            return messagePopup('Failed to generate: ' + result.message)

        messagePopup(`Generate: ${result.message}`)
        outputImage.value = `data:image/png;base64,${result.image}`
    } catch (error) {
        return messagePopup(`Generate error: ${error}`)
    }
}

function triggerFileInput() { fileInputRef.value?.click() }

function handleFileSelect(event: Event) {
    const input = event.target as HTMLInputElement
    if (input.files && input.files[0]) {
        const file = input.files[0]
        
        const reader = new FileReader()
        reader.onload = (e) => {
            inputImage.value = e.target?.result as string
        }
        reader.readAsDataURL(file)
        
        messagePopup('Up load image', 1000)
    }
}

function showViewer() {
    showView.value = outputImage.value ? true : false
}

function closeViewer() { showView.value = false }
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