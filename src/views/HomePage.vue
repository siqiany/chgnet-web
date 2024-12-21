<template>
    <div>
      <FileButton />
      <select v-model="predictionType" @change="handlePredictionTypeChange">
        <option value="DirectInference">Direct Inference</option>
        <option value="MolecularDynamics">Molecular Dynamics</option>
        <option value="StructureOptimization">Structure Optimization</option>
      </select>
      <button @click="runPrediction">Run CHGnet</button>
    </div>
  </template>
  
  <script>
  import FileButton from '@/components/FileButton.vue';
  import { mapGetters } from 'vuex';

  export default {
    components: {
      FileButton
    },
    computed: {
     ...mapGetters(['getSelectedFile'])
    },
    data() {
      return {
        predictionType: ''
      };
    },
    methods: {
      handlePredictionTypeChange() {
            const file = this.getSelectedFile;
            if (file) {
                console.log('About to navigate, selected file in Home.vue:', file);
                this.$router.push({ name: this.predictionType });
            } else {
                console.error('没有有效的文件对象可用于传递，请检查文件选择情况。');
            }
        }
    }
  };
  </script>
  