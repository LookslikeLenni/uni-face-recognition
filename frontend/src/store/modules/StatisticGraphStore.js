/* 
@app.get("/timetogether/{user1}/{user2}/")
def get_user_time_together(user1: int, user2: int, db: Session = Depends(get_db)):
 
@app.get("/time/{user_id}")
def get_user_time(user_id: int, db: Session = Depends(get_db)):

Graph with all users as nodes and edges scaling with time spent together
*/

// frontend/src/components/StatisticGraphStore.js


/**
 * @typedef {Object} GraphState
 * @property {Object} graphData
 * @property {Array<{ id: number; name: string; size: number }>} graphData.nodes
 * @property {Array<{ source: number; target: number; value: number }>} graphData.links
 */


export default {
  namespaced: true,
  state: {
    nodes: [],
    links: [],
  },
  mutations: {
    setNodes(state, nodes) {
      state.nodes = nodes;
    },
    setLinks(state, links) {
      state.links = links;
    },
  },
  actions: {
    async getGraphData({ state, commit, dispatch, rootState }) {
      const nodes = [];
      const links = [];

      if (!rootState.users || rootState.users.length === 0) {
        await dispatch('fetchUsers', null, { root: true });
      }

      const users = rootState.users || [];
      const userCount = users.length;

      for (let i = 0; i < userCount; i++) {
        const response = await fetch(`http://127.0.0.1:8000/time/${users[i].id}`);
        const data = await response.json();
        nodes.push({ id: users[i].id, name: users[i].first_name, timeInFrame: data });
        for (let j = i + 1; j < userCount; j++) {
          const responseTogether = await fetch(`http://127.0.0.1:8000/timetogether/${users[i].id}/${users[j].id}`);
          const dataTogether = await responseTogether.json();
          links.push({ source: users[i].id, target: users[j].id, timeTogether: dataTogether });
        }
      }

      commit('setNodes', nodes);
      commit('setLinks', links);
      console.log('New graph data:', { nodes, links });
    }
  }
};


    

    

