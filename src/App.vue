<template>
<div class='App'>
    <div class='header'>
        <h2>PeanutsZheng.ai</h2>

        <button class='themeBtn' @click='toggleTheme'>
            <img v-if="currentTheme === 'latte'" src='./assets/icons/cil-lightbulb.png' title="change theme" />
            <img v-else-if="currentTheme === 'frappe'" src='./assets/icons/cil-moon.png' title="change theme" />
        </button>
    </div>

    <div class='container'>
        <div class='menu'>
            <RouterLink to="/" class="menu-item">Home</RouterLink>
            <RouterLink to="/chat" class="menu-item">Chat</RouterLink>
            <RouterLink to="/draw" class="menu-item">Draw</RouterLink>
            <RouterLink to="/about" class="menu-item">About</RouterLink>
        </div>
        <div class='content'>
            <RouterView v-slot="{ Component }">
                <transition name="fade" mode="out-in">
                    <component :is="Component" :key="$route.fullPath" />
                </transition>
            </RouterView>
        </div>
    </div>

    <div class='footer'>
        peanutszheng &copy; 2025
    </div>
</div>
</template>

<script setup name='App' lang='ts'>
import { RouterLink, RouterView } from 'vue-router'
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'

type ITheme = 'latte' | 'frappe'
const currentTheme = ref<ITheme>('latte')
const route = useRoute()

const componentStylesMap: Record<string, string[]> = {
  '/': ['home.css'],
  '/chat': ['chat.css', 'popup.css', 'ctrlPanel.css'],
  '/draw': ['draw.css', 'popup.css', 'ctrlPanel.css'],
  '/about': ['home.css']
}


onMounted(() => {
    let savedTheme = localStorage.getItem('theme') as ITheme | 'latte'

    currentTheme.value = savedTheme
    applyTheme(savedTheme)
})

watch(route, () => { 
    setTimeout(() => {
        loadComponentStyles(currentTheme.value)
    }, 50)
})

// ==== FUNCTIONS ==== //
function toggleTheme() {
    const newTheme = currentTheme.value === 'latte' ? 'frappe' : 'latte'

    preloadComponentStyles(newTheme).then(() => {
        currentTheme.value = newTheme
        applyTheme(newTheme)
        localStorage.setItem('theme', newTheme)
    })
}

function preloadComponentStyles(theme: ITheme): Promise<void> {
    return new Promise((resolve) => {
        const neededStyles = componentStylesMap[route.path] || []
        
        if (neededStyles.length === 0) {
            resolve()
            return
        }

        let loadedCount = 0
        const totalStyles = neededStyles.length

        neededStyles.forEach(style => {
            const link = document.createElement('link')
            link.rel = 'preload'
            link.as = 'style'
            link.href = `/src/assets/css/${theme}/${style}`
            link.onload = link.onerror = () => {
                loadedCount++
                if (loadedCount === totalStyles)
                    resolve()
            }
            document.head.appendChild(link)
        })
    })
}

function loadComponentStyles(theme: ITheme) {
    const neededStyles = componentStylesMap[route.path] || []
    
    // Load component styles
    neededStyles.forEach(style => {
        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = `/src/assets/css/${theme}/${style}`
        link.setAttribute('data-component-style', style)
        document.head.appendChild(link)
    })
}

function applyTheme(theme: ITheme) {
    // Load new theme
    const newLink = document.createElement('link')
    newLink.rel = 'stylesheet'
    newLink.href = `/src/assets/css/${theme}/app.css`
    newLink.setAttribute('data-theme', theme)
    
    newLink.onload = () => {
        // Fade out
        document.body.style.opacity = '0'

        // Remove existing links and component styles
        const existingComponentLinks = document.querySelectorAll('link[data-component-style]')
        setTimeout(() => { existingComponentLinks.forEach(link => link.remove()) })

        const existingLinks = document.querySelectorAll('link[data-theme]')
        existingLinks.forEach(link => { if (link !== newLink) link.remove() })

        document.body.className = `theme-${theme}`
        loadComponentStyles(theme)

        // Fade in
        document.body.style.transition = 'opacity 0.2s ease'
        document.body.style.opacity = '1'
    }
    
    document.head.appendChild(newLink)
}
</script>

<style scoped>
/* fade in and fade out */
.fade-enter-active, .fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
    opacity: 0;
}

* {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
</style>