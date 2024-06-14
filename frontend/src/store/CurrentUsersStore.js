export default {
    namespaced: true,
    state: {
        currentUsers: [],
        isMuted: false,
        logs: []
    },

    mutations: {
        addUser(state, user) {
            const userExists = state.currentUsers.some(existingUser => existingUser.id === user.id);
            if (user.first_name === "Unknown" || userExists) {
                return;
            }
            state.currentUsers.push(user);
            console.log('New currentUsers:', state.currentUsers);
        },
        removeUser(state, user) {
            state.currentUsers = state.currentUsers.filter((existingUser) => existingUser.id !== user.id);
        },
        SET_MUTE_STATUS(state, status) {
            state.isMuted = status;
        },
        setLogs(state, logs) {
            state.logs = logs;
        },
        addLog(state, log) {
            state.logs.push(log);
        },
    
    },

    actions: {
        async fetchCurrents({ commit, dispatch, state }) {
            try {
                const response = await fetch('http://127.0.0.1:8000/current/');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                console.log("New data:" + data);

                if (data.length === 0) {
                    return;
                }
                
                data.forEach((user) => {
                    dispatch('addUserThenRemove', user);
                });
            } catch (error) {
                console.error(error);
            }
        },    
        addUserThenRemove({ commit, state }, user) {
            const userExists = state.currentUsers.some(existingUser => existingUser.id === user.id);
            if (user.first_name !== "Unknown" && !userExists) {
                commit('addUser', user);
            
                setTimeout(() => {
                    commit('removeUser', user);
                }, 15000);
            }
        },
        async fetchLogs({ commit }) {
            try {
                // console.log("Fetching logs");
              const response = await fetch('http://127.0.0.1:8000/current/');
              const data = await response.json();
        
              // Add a timestamp to each log
              const logsWithTimestamps = data.map(log => ({
                ...log,
                timestamp: new Date().toLocaleString(),
              }));
        
              // Commit each log individually
            logsWithTimestamps.forEach(log => {
                commit('addLog', log);
            });
            } catch (error) {
              console.error(error);
            }
        },
    },
    getters: {
        isMuted:state =>  state.isMuted,
    },
};