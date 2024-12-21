<template>
    <form @submit.prevent="onSubmit">
      <label>Ensemble</label>
      <input type="text" v-model="ensemble" />
      <label>Temperature (K)</label>
      <input type="number" v-model="temperature" />
      <label>Time Step (fs)</label>
      <input type="number" v-model="timestep" step="0.1" />
      <label>Trajectory File</label>
      <input type="text" v-model="trajectory" />
      <label>Log File</label>
      <input type="text" v-model="logfile" />
      <label>Log Interval</label>
      <input type="number" v-model="loginterval" />
      <label>Number of Steps</label>
      <input type="number" v-model="steps" />
      <label>Device</label>
      <select v-model="device">
        <option value="cpu">cpu</option>
        <option value="cuda">cuda</option>
      </select>
      <button type="submit">Run Molecular Dynamics</button>
    </form>
  </template>
  
  <script>
  export default {
    data() {
      return {
        ensemble: 'nvt',
        temperature: 1000,
        timestep: 2,
        trajectory: 'md_out.traj',
        logfile: 'md_out.log',
        loginterval: 100,
        steps: 50,
        device: 'cpu'
      };
    },
    methods: {
      onSubmit() {
        const mdParams = {
          ensemble: this.ensemble,
          temperature: this.temperature,
          timestep: this.timestep,
          trajectory: this.trajectory,
          logfile: this.logfile,
          loginterval: this.loginterval,
          steps: this.steps,
          device: this.device
        };
        this.$emit('submit', mdParams);
      }
    }
  };
  </script>
  