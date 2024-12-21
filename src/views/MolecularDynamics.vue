<template>
    <div>
      <h2>Molecular Dynamics Parameters</h2>
      <MDParamsForm @submit="runMolecularDynamics" />
      <ResultDisplay :result="result" />
      <FileDownload :file1="fileObj1" :file2="fileObj2" />
    </div>
  </template>
  
  <script>
  import MDParamsForm from '@/components/MDParamsForm.vue';
  import ResultDisplay from '@/components/ResultDisplay.vue';
  import FileDownload from '@/components/DownloadFile.vue';
  import { mapGetters} from 'vuex';
  import { runMolecularDynamics as apiRunMolecularDynamics } from '@/api/chgnet-api.js';
  
  export default {
    components: {
      MDParamsForm,
      ResultDisplay,
      FileDownload
    },
    computed: {
     ...mapGetters(['getSelectedFile'])
    },
    data() {
      return {
        result: '',
        fileObj1:null,
        fileObj2:null
      };
    },
    methods: {
      async runMolecularDynamics(mdParams) {
        const file = this.getSelectedFile;
        console.log('mdparams',mdParams);
        try {
          const response = await apiRunMolecularDynamics(file, mdParams);
          this.result = response.message;
          this.fileObj1 = new File([response.trajectory.content], response.trajectory.name);
          this.fileObj2 = new File([response.logfile.content], response.logfile.name);
          console.log(response);
          console.log('获取到的文件1:', this.fileObj1);
          console.log('获取到的文件2:', this.fileObj2);
          if (!this.fileObj1.name ||!this.fileObj2.name) {
            console.error('文件对象的name属性存在问题,请检查文件获取逻辑');
          }
        } catch (error) {
          this.result = `Error: ${error.message}`;
        }
      }
    }
  };
  </script>
  