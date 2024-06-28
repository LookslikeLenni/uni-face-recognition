/**
 * @typedef {Object} GraphState
 * @property {Object} graphData
 * @property {Array<{ id: number; name: string; size: number }>} graphData.nodes
 * @property {Array<{ source: number; target: number; value: number }>} graphData.edges
 */

export default {
  namespaced: true,
  state: {
    nodes: [],
    edges: [],
  },
  mutations: {
    setNodes(state, nodes) {
      state.nodes = nodes;
    },
    setEdges(state, edges) {
      state.edges = edges;
    },
  },
  actions: {
    async getGraphData({ commit, dispatch, rootState }) {
      const nodes = {};
      const edges = {};
      const nodeMap = {};

      if (!rootState.users || rootState.users.length === 0) {
        await dispatch('fetchUsers', null, { root: true });
      }

      const users = rootState.users || [];
      const userCount = users.length;

      // First create all nodes and populate the nodeMap
      for (let i = 0; i < userCount; i++) {
        const response = await fetch(`http://127.0.0.1:8000/time/${users[i].id}`);
        const data = await response.json();
        const node = { 
          id: users[i].id, 
          name: `${users[i].first_name} ${users[i].last_name}`, // Combine first_name and last_name
          timeInFrame: data
        };
        nodes[`node${i + 1}`] = node;
        nodeMap[users[i].id] = `node${i + 1}`;
      }

      // Then create the edges
      const fetchEdges = [];
      let edgeCount = 1;
      for (let i = 0; i < userCount; i++) {
        for (let j = i + 1; j < userCount; j++) {
          fetchEdges.push(
            fetch(`http://127.0.0.1:8000/timetogether/${users[i].id}/${users[j].id}`)
              .then(response => response.json())
              .then(dataTogether => {
                if (dataTogether && dataTogether > 0) {
                  edges[`edge${edgeCount}`] = {
                    source: nodeMap[users[i].id],
                    target: nodeMap[users[j].id],
                    width: Math.min(10, Math.max(1, dataTogether / 10)), // Scale width
                    color: "red",
                    timeTogether: Math.round(dataTogether * 100) / 100 // Save time together, rounded to 2 decimals
                  };
                  edgeCount++;
                }
              })
          );
        }
      }

      await Promise.all(fetchEdges);

      commit('setNodes', nodes);
      commit('setEdges', edges);
    }
  },

  getters: {
    getLeaderboard(state) {
      const leaderboard = [];
      for (const nodeKey in state.nodes) {
        if (state.nodes.hasOwnProperty(nodeKey)) {
          const node = state.nodes[nodeKey];
          leaderboard.push({ id: node.id, name: node.name, timeInFrame: node.timeInFrame });
        }
      }
      return leaderboard.sort((a, b) => b.timeInFrame - a.timeInFrame);
    }
  }
};
