import { createRouter, createWebHistory } from 'vue-router';
import Home from '@/views/HomePage.vue';
import DirectInference from '@/views/DirectInference.vue';
import MolecularDynamics from '@/views/MolecularDynamics.vue';
import StructureOptimization from '@/views/StructureOptimization.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/DirectInference',
    name: 'DirectInference',
    component: DirectInference
  },
  {
    path: '/MolecularDynamics',
    name: 'MolecularDynamics',
    component: MolecularDynamics
  },
  {
    path: '/StructureOptimization',
    name: 'StructureOptimization',
    component: StructureOptimization
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
