<template>
  <input type="file" @change="onFileChange" />
</template>

<script>
import { mapMutations } from 'vuex';

export default {
  methods: {
   ...mapMutations(['setSelectedFile']),
      onFileChange(event) {
          const file = event.target.files[0];
          if (file) {
              console.log('在文件选择组件中成功选择文件:', file);
              this.setSelectedFile(file);
          }
      }
  }
};
</script>
