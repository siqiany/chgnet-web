<template>
  <div id="app">
   <header>
      <h1>NJMatLab</h1>
   </header>
    <nav>
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/DirectInference">DirectInference</router-link></li>
        <li><router-link to="/MolecularDynamics">MolecularDynamics</router-link></li>
        <li><router-link to="/StructureOptimization">StructureOptimization</router-link></li>
      </ul>
    </nav>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>

export default {
  name: 'App',
};
</script>

<style>
/* 添加一些全局样式 */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #4a6581;
  margin-top: 60px;
}

header {
  background-color: #0c0c0c;
  color: white;
  text-align: left;
  padding-left: 10px;
  align-items: center;
}

nav {
  display: flex;
  justify-content: center;
  background-color: #312d2d;
}

nav ul {
  list-style-type: none;
  padding: 0;
}
 
nav li {
  display: inline;
  margin: 0 10px;
}
 
nav a {
  text-decoration: none;
  color: #eaf0ee;
}
 
nav a.router-link-exact-active, nav a:hover {
  color: #5a4940;
}
 
main {
  padding: 20px;
}
</style>