import { createStore } from 'vuex';//暂时没有，但未来扩展有用

const store = createStore({
  state: {
    // 存储文件数据的状态
    files: {
        file1:null,
        file2:null
    }
  },
  mutations: {
    // 设置文件数据的 mutation
    SET_FILE(state, file) {
      state.files.file1 = file;
    },
    SET_FILE(state, file) {
        state.files.file2 = file;
      }
  },
  actions: {
    // 异步设置文件数据的 action，可用于在组件中分发
    setFile1({ commit }, file) {
      commit('SET_FILE1', file);
    },
    setFile2({ commit }, file) {
        commit('SET_FILE2', file);
      }
  },
  getters: {
    // 获取文件数据的 getter
    getFile1: state => state.files.file1,
    getFile2: state => state.files.file2
  }
});

export default store;
