import { createRouter, createWebHistory } from "vue-router"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'Home',
            component: () => import('../views/Home.vue')
        },
        {
            path: '/chat',
            name: 'Chat',
            component: () => import('../views/Chat.vue')
        },
        {
            path: '/draw',
            name: 'Draw',
            component: () => import('../views/Draw.vue')
        },
        {
            path: '/about',
            name: 'About',
            component: () => import('../views/About.vue')
        }
    ]
})

export default router