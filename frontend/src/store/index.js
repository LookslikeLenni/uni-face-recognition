import { createStore } from 'vuex'
import CurrentUsersStore from './modules/CurrentUsersStore'
import StatisticGraphStore from './modules/StatisticGraphStore'

export default createStore({
    state: {
        users: [],
    },
    mutations: {
        setUsers(state, users) {
            state.users = users;
        }
    },
    actions: {
        async fetchUsers({ commit }) {
            try {
                const response = await fetch('http://127.0.0.1:8000/users/');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                /* console.log("New data:", data);
                console.log("Data length:", data.length);
                console.log("First user:", data[0]); */
                commit('setUsers', data);
                //console.log("commit went through");
            }
            catch (error) {
                console.error(error);
            }
        }
    },
    modules: {
        CurrentUsersStore,
        StatisticGraphStore,
    }
})
