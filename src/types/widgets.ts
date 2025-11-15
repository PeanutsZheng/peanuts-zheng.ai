export interface IWidget {
    label: string
    component: string // Component name, ep.'input'
    props: Record<string, any> // Props, e.p { type: 'range', min: 0, max: 100 }
    events?: Record<string, Function> // Events, e.p { change: (val) => {} }
}