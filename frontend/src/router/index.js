import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/pages/HomePage.vue';
import CustomersPage from '@/pages/CustomersPage.vue';
import FinancialReportPage from '@/pages/FinancialReportPage.vue';

const routes = [
    { path: '/', name: 'Home', component: HomePage },
    { path: '/customers', name: 'Customers', component: CustomersPage},
    { path: '/financial-report', name: 'FinancialReport', component: FinancialReportPage},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
