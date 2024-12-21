<template>
  <div>
    <ResultDisplay :result="result" v-html="result" />
  </div>
</template>

<script>
import ResultDisplay from '@/components/ResultDisplay.vue';
import { mapGetters } from 'vuex';
import { runDirectInference as apiRunDirectInference } from '@/api/chgnet-api.js';

export default {
  components: {
    ResultDisplay
  },
  computed: {
     ...mapGetters(['getSelectedFile'])
    },
  data() {
    return {
      result: ''
    };
  },
  async mounted() {
    const file = this.getSelectedFile;
    try {
      const response = await apiRunDirectInference(file);
      if (response && typeof response === 'object') {
            // 检查各个属性是否存在且类型符合预期（这里简单判断非null和undefined，实际可根据具体数据类型进一步验证）
            let forces = '未获取到力相关数据，请检查后端返回格式或联系管理员';
            if (Array.isArray(response.forces)) {
              const formattedForces = response.forces.map(vector => `(${vector.join(', ')})`).join('<br>');
              forces = formattedForces;
              console.log('向量化后的forces:',forces);
            }

            const energy = response.energy!== null && response.energy!== undefined? response.energy : '暂无能量数据';
            const stress = response.stress? response.stress.map(vector => `(${vector.join(', ')})`).join('<br>') : '未获取到应力相关数据，请检查后端返回格式或联系管理员';
            const magmom = response.magmom? response.magmom.map(vector => `(${vector.join(', ')})`).join('<br>') : '未获取到磁矩相关数据，请检查后端返回格式或联系管理员';

            this.result = `CHGNet-predicted energy (eV/atom):<br>${energy}<br><br>CHGNet-predicted forces (eV/A):<br>${forces}<br><br>CHGNet-predicted stress (GPa):<br>${stress}<br><br>CHGNet-predicted magmom (mu_B):<br>${magmom}<br><br>`;
        } else {
            this.result = '获取预测结果出现问题，请稍后重试或联系管理员。';
        }
    } catch (error) {
        this.result = `Error: ${error.message}`;
    }
  }
};
</script>
