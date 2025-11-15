<template>
<div class='CtrlPanel' :class="{show: isPanelVisible}">
    <button id="toggleCtrlBtn" @click="toggleCtrlPanel">
        <img :src="toggleIcon" title="Show / hide ctrl panel">
    </button>


    <div v-if="hoveredSlider" class="slider-value" style="display: block;"
        :style="getSliderPosition(hoveredSlider.element)">
        {{ hoveredSlider.value }}  <!-- Element for show slider value -->
    </div>

    <div v-show="isPanelVisible" class="ctrl-container">
        <div v-for="(widget, index) in renderedWidgets" :key="index" class="ctrl-widget">
            <component :is="widget" />
        </div>
    </div>
</div>
</template>

<script setup name='CtrlPanel' lang='ts'>
import { ref, computed, onMounted, h } from 'vue'
import leftIcon from '../assets/icons/cil-chevron-left.png'
import rightIcon from '../assets/icons/cil-chevron-right.png'
import { type IWidget } from '../types/widgets'

const props = defineProps<{ widgets?: IWidget[] }>()
const widgets = ref<IWidget[]>([])
const isPanelVisible = ref(false)
const toggleIcon = computed(() => { return isPanelVisible.value ? rightIcon : leftIcon })
const hoveredSlider = ref<{element: HTMLElement, value: string} | null>(null)

// Initial widgets
onMounted(() => { if (props.widgets) widgets.value.push(...props.widgets) })
const renderedWidgets = computed(() => {
  return widgets.value.map(widget => renderWidget(widget))
})

defineExpose({ setValue, getValues, registerEventHandler })

// Functions
function toggleCtrlPanel() { isPanelVisible.value = !isPanelVisible.value }

function renderWidget(widget: IWidget) {
    // Button widget
    if (widget.component === 'button')
        return renderBottonWidget(widget)

    // Select widget
    if (widget.component === 'select')
        return renderSelectWidget(widget)

    // Other widgets
    return renderOtherWidget(widget)
}

function registerEventHandler(label: string, eventName: string, handler: Function) {
    const widget = widgets.value.find(w => w.label === label)

    if (!widget) return

    if (!widget.events)
        widget.events = {}

    widget.events[eventName] = handler
}

function setValue(label: string, props: any) {
    const widget = widgets.value.find(w => w.label === label)
    if (!widget)
        return

    const element = document.querySelector(`[data-label="${widget.label}"]`)
    if (!element)
        return

    if (element instanceof HTMLInputElement) {
        if (element.type === 'checkbox' && typeof(props) === 'boolean')
            element.checked = props || false
        else
            element.value = props || null
    }
    else if (element instanceof HTMLSelectElement)
        element.value = props || null
    else if (element instanceof HTMLTextAreaElement)
        element.value = props || null
}

function getValues() {
    const values: Record<string, string | number | boolean | null> = {}
    
    for (const widget of widgets.value) {
        if (!widget.label)
            continue

        const element = document.querySelector(`[data-label="${widget.label}"]`)
        if (!element)
            continue

        if (element instanceof HTMLInputElement) {
            if (element.type === 'checkbox')
                values[widget.label] = element.checked
            else if (element.type === 'radio') {
                if (element.checked)
                    values[widget.label] = element.value
            } else
                values[widget.label] = element.value
        }
        else if (element instanceof HTMLSelectElement)
            values[widget.label] = element.value
        else if (element instanceof HTMLTextAreaElement)
            values[widget.label] = element.value
        else
            values[widget.label] = null
    }
    
    return values
}

function renderBottonWidget(widget: IWidget) {
    const { onClick, ...buttonProps } = widget.props || {}
    const eventHandlers: Record<string, Function> = {}

    if (widget.events?.onClick)
        eventHandlers['onClick'] = widget.events.onClick
    else
        eventHandlers['onClick'] = () => {}

    return h('div', {}, [
        widget.label ? h('label', widget.label) : null,
        h('button', { ...buttonProps, ...eventHandlers }, widget.props?.innerText || 'Button')
    ])
}

function renderSelectWidget(widget: IWidget) { 
    const { options, ...selectProps } = widget.props || {}
    const selectPropsWithLabel = {
        ...selectProps,
        ...(widget.label ? { 'data-label': widget.label } : {})
    }

    // Other event handlers
    const eventHandlers: Record<string, Function> = {}
    if (widget.events) {
        Object.keys(widget.events).forEach(event => {
            const handler = widget.events![event];
            if (typeof handler === 'function') {
                eventHandlers[event] = (e: Event) => handler(e);
            }
        })
    }

    return h('div', {}, [
        widget.label ? h('label', widget.label) : null,
        h('select', { ...selectPropsWithLabel, ...eventHandlers }, [
            ...(options || []).map((option: { value: string, label?: string }) => 
            h('option', { value: option.value }, option.label || option.value)
            )
        ])
    ])
}

function renderOtherWidget(widget: IWidget) {
    const widgetProps = {
    ...widget.props,
    ...(widget.label ? { 'data-label': widget.label } : {})
    }

    const eventHandlers: Record<string, Function> = {}
    // Other event handlers
    if (widget.events) {
        Object.keys(widget.events).forEach(event => {
            const handler = widget.events![event];
            if (typeof handler === 'function') {
                eventHandlers[event] = handler;
            }
        })
    }

    // Default add show value event for input[type="range"]
    if (widget.component === 'input' && widget.props.type === 'range') {
        eventHandlers['onMouseenter'] = handleSliderMouseEnter
        eventHandlers['onMouseleave'] = handleSliderMouseLeave
    }

    return h('div', {}, [
        widget.label ? h('label', widget.label) : null,
        h(widget.component, { ...widgetProps, ...eventHandlers })
    ])
}

function handleSliderMouseEnter(event: Event) {
    // Get hoverd slider element
    const target = event.target as HTMLInputElement
    hoveredSlider.value = {
        element: target,
        value: target.value
    }
}

function handleSliderMouseLeave() { hoveredSlider.value = null }

function getSliderPosition(sliderElement: HTMLElement) {
    const rect = sliderElement.getBoundingClientRect()
    const containerRect = sliderElement.closest('.CtrlPanel')?.getBoundingClientRect()
    
    if (!containerRect) return { top: '0px', left: '0px' }

    const top = rect.top - containerRect.top + rect.height / 2 - 10
    const left = rect.right - containerRect.left + 10
    
    return { top: `${top}px`, left: `${left}px` }
}
</script>

<style scoped>
* {
    transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}
</style>