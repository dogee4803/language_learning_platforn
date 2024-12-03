import { createRouter, createWebHistory } from 'vue-router';
import CustomersPage from '@/pages/CustomersPage.vue';
import FinancialReportPage from '@/pages/FinancialReportPage.vue';
import HomePage from '@/pages/HomePage.vue';
import LoginPage from '@/pages/LoginPage.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/customers',
    name: 'Customers',
    component: CustomersPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/financial-report',
    name: 'FinancialReport',
    component: FinancialReportPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Защита маршрутов
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  
  if (to.meta.requiresAuth && !token) {
    // Сохраняем путь, с которого пользователь пришел
    localStorage.setItem('redirectPath', to.fullPath);
    // Перенаправляем на страницу входа
    next({ 
      path: '/login',
      query: { redirect: to.fullPath }
    });
  } else if (to.path === '/login' && token) {
    // Если пользователь авторизован и пытается зайти на страницу входа
    next('/');
  } else {
    next();
  }
});

export default router;
