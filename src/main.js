import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createStore } from 'vuex'

const store = createStore({
    state() {
        return {
            selectedFile: null
        }
    },
    mutations: {
        setSelectedFile(state, file) {
            state.selectedFile = file;
        }
    },
    actions: {
    },
    getters: {
        getSelectedFile: (state) => state.selectedFile
    }
})

const app = createApp(App)
app.use(store)
app.use(router)
app.mount('#app')
