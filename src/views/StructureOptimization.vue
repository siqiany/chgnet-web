<template>
    <div>
      <ResultDisplay :result="result" v-html="result" />
    </div>
  </template>
  
  <script>
  import ResultDisplay from '@/components/ResultDisplay.vue';
  import { mapGetters } from 'vuex';
  import { runStructureOptimization as apiRunStructureOptimization } from '@/api/chgnet-api.js';
  
  function formatLatticeInfo(latticeData) {
    const latticeMatrix = latticeData.lattice.matrix;
    let latticeInfo = '晶格矩阵信息：<br>';
    latticeMatrix.forEach((row, rowIndex) => {
        const formattedRow = row.map(num => num.toFixed(6)).join(' &nbsp;&nbsp;&nbsp; '); // 格式化每个数值保留一定小数位，并用空格隔开元素，方便展示
        latticeInfo += `第 ${rowIndex + 1} 行：${formattedRow}<br>`;
    });
    latticeInfo += `晶格周期性边界条件(pbc):${latticeData.lattice.pbc}<br>`;
    latticeInfo += `晶格参数 a:${latticeData.lattice.a.toFixed(6)},b:${latticeData.lattice.b.toFixed(6)},c:${latticeData.lattice.c.toFixed(6)}<br>`;
    latticeInfo += `晶格角度 alpha:${latticeData.lattice.alpha.toFixed(6)},beta:${latticeData.lattice.beta.toFixed(6)},gamma:${latticeData.lattice.gamma.toFixed(6)}<br>`;
    return latticeInfo;
}

function formatAtomsInfo(atomsData) {
    let atomsInfo = '原子信息：<br>';
    atomsData.forEach((atom, atomIndex) => {
        atomsInfo += `原子 ${atomIndex + 1}:<br>`;
        atomsInfo += `元素种类：${atom.species[0].element}<br>`;
        atomsInfo += `占有率(occu):${atom.species[0].occu}<br>`;
        atomsInfo += `分数坐标(abc):${atom.abc.join(' &nbsp;&nbsp;&nbsp; ')}<br>`;
        atomsInfo += `磁矩(magmom):${atom.properties.magmom}<br>`;
        atomsInfo += `笛卡尔坐标(xyz):${atom.xyz.join(' &nbsp;&nbsp;&nbsp; ')}<br><br>`;
    });
    return atomsInfo;
}


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
        if (file) {
            console.log("OK");
            console.log('传递中的文件:',file);
            const apiResult = await apiRunStructureOptimization(file);

            const myObject = apiResult.final_structure;
            const dataToParse = JSON.stringify(myObject); // 这里是你之前获取并处理后的准备用于JSON解析的数据哦，根据实际情况可能有替换引号等操作在前了
            console.log(dataToParse);
            console.log('准备用于JSON解析的数据:', dataToParse);
            try {
              const processedData = JSON.stringify(JSON.parse(dataToParse));
              console.log('准备用于JSON解析的数据:', processedData);
              const finalStructure = JSON.parse(processedData);
              //后续对解析后的数据进行处理等逻辑继续写在这里哦
              let finalStructureInfo = '未获取到最终结构相关数据，请检查后端返回格式或联系管理员';
              const latticeInfo = formatLatticeInfo(finalStructure);
              const atomsInfo = formatAtomsInfo(finalStructure.sites);
              finalStructureInfo = `${latticeInfo}<br><br>${atomsInfo}`;
              this.result = `CHGNet relaxed structure:<br>${finalStructureInfo}<br><br>relaxed total energy in eV:${apiResult.relaxed_total_energy}`;
            } catch (parseError) {
              console.error('解析JSON数据时出错:', parseError);
            }
        } else {
            this.result = '未获取到有效的文件参数，请检查文件选择及路由传递情况。';
        }
    }
  };
  </script>
  