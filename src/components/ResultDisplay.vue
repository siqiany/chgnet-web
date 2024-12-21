<template>
    <div v-if="result">{{ result }}</div>
  </template>
  
  <script>
  export default {
    props: ['result']
  };
  </script>
  