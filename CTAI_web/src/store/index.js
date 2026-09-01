import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
        isLoggedIn: false,
        user: null
    },
    mutations: {
        LOGIN(state, user) {
            state.isLoggedIn = true
            state.user = user
        },
        LOGOUT(state) {
            state.isLoggedIn = false
            state.user = null
        }
    },
    actions: {
        login({ commit }, user) {
            // 模拟登录逻辑
            return new Promise((resolve, reject) => {
                setTimeout(() => {
                    if (user.username === 'admin' && user.password === '123456') {
                        commit('LOGIN', user)
                        resolve()
                    } else {
                        reject(new Error('Invalid username or password'))
                    }
                }, 1000)
            })
        },
        logout({ commit }) {
            commit('LOGOUT')
        }
    }
})
