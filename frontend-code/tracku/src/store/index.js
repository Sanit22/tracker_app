import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
    state: {
        access_token: '',
    },
    mutations: {
        setAuthToken (state, token) {
            state.access_token = token
        }
    },
})  