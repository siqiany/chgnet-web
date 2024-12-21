<template>
    <div>
      <button @click="downloadFile1" :disabled="!file1">download trajectory file</button>
      <button @click="downloadFile2" :disabled="!file2">download log file</button>
    </div>
  </template>
  
  <script>
  
  export default{
    props: ['file1', 'file2'],
    methods: {
      downloadFile1(){
        if (this.file1) {
          console.log('看看下载文件',this.file1);
          const url = URL.createObjectURL(this.file1);
          const a = document.createElement('a');
          a.href = url;
          a.download = this.file1.name;
          a.click();
          URL.revokeObjectURL(url);
        }
        else{
          console.log('下载文件出现问题ww',this.file1);
        }
      },
      downloadFile2(){
        if (this.file2) {
          const url = URL.createObjectURL(this.file2);
          const a = document.createElement('a');
          a.href = url;
          a.download = this.file2.name;
          a.click();
          URL.revokeObjectURL(url);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  button {
    padding: 8px 16px;
    border: none;
    background-color: #007bff;
    color: white;
    cursor: pointer;
  }
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  