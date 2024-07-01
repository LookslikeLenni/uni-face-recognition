import { createStore } from 'vuex'
import CurrentUsersStore from './modules/CurrentUsersStore'
import StatisticGraphStore from './modules/StatisticGraphStore'

export default createStore({
    state: {
        users: [],
        knownUsers: [],
        unknownUsers: []
    },
    mutations: {
        setUsers(state, users) {
            state.users = users;
        },
        setKnownUsers(state, users) {
            state.knownUsers = users;
        },
        setUnknownUsers(state, users) {
            state.unknownUsers = users;
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
                commit('setUsers', data);

                const knownUsers = data.filter(user => user.first_name !== "Unknown" || user.last_name !== "");
                const unknownUsers = data.filter(user => user.first_name === "Unknown" && user.last_name === "");
                commit('setKnownUsers', knownUsers);
                commit('setUnknownUsers', unknownUsers);
            }
            catch (error) {
                console.error(error);
            }
        },
    },
    modules: {
        CurrentUsersStore,
        StatisticGraphStore,
    }
});
