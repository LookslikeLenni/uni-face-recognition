import './assets/main.css'

import { createApp } from 'vue'
import { createStore } from 'vuex'
import App from './App.vue'
import router from './router'

import CurrentUsersStore from './store/CurrentUsersStore'


const app = createApp(App)

app.use(router)

const store = createStore({
    modules: {
        CurrentUsersStore
    }
})

app.use(store)

app.mount('#app')
