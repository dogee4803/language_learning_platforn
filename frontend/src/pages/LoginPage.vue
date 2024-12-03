<template>
  <div class="flex align-items-center justify-content-center min-h-screen bg-gray-100">
    <div class="surface-card p-4 shadow-2 border-round w-full max-w-30rem mx-auto">
      <h2 class="text-center text-2xl mb-4">Вход в систему</h2>
      
      <div class="mb-4">
        <span class="p-float-label w-full">
          <Prime-InputText 
            id="username" 
            v-model="username" 
            class="w-full" 
            :class="{ 'p-invalid': errors.username }"
          />
          <label for="username">Имя пользователя</label>
        </span>
        <small class="p-error block mt-1" v-if="errors.username">{{ errors.username }}</small>
      </div>

      <div class="mb-4">
        <span class="p-float-label w-full">
          <Prime-Password 
            id="password" 
            v-model="password" 
            class="w-full" 
            :feedback="false"
            :toggleMask="true"
            :class="{ 'p-invalid': errors.password }"
          />
          <label for="password">Пароль</label>
        </span>
        <small class="p-error block mt-1" v-if="errors.password">{{ errors.password }}</small>
      </div>

      <div v-if="errorMessage" class="mb-4">
        <Prime-Message severity="error">{{ errorMessage }}</Prime-Message>
      </div>

      <Prime-Button 
        label="Войти" 
        @click="login" 
        class="w-full"
        :loading="loading"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import api from '@/services/api';

const router = useRouter();
const toast = useToast();

const username = ref('');
const password = ref('');
const loading = ref(false);
const errors = ref({});
const errorMessage = ref('');

const validateForm = () => {
  const newErrors = {};
  
  if (!username.value) {
    newErrors.username = 'Введите имя пользователя';
  }
  
  if (!password.value) {
    newErrors.password = 'Введите пароль';
  }
  
  errors.value = newErrors;
  return Object.keys(newErrors).length === 0;
};

const login = async () => {
  if (!validateForm()) return;
  
  loading.value = true;
  errorMessage.value = '';
  
  try {
    console.log('Отправка данных:', {
      username: username.value,
      password: password.value
    });
    
    const response = await api.post('auth/login/', {
      username: username.value,
      password: password.value
    });
    
    console.log('Ответ сервера:', response.data);
    
    // Сохраняем токен в localStorage
    localStorage.setItem('token', response.data.token);
    
    // Устанавливаем токен для всех последующих запросов
    api.defaults.headers.common['Authorization'] = `Token ${response.data.token}`;
    
    toast.add({
      severity: 'success',
      summary: 'Успешно',
      detail: 'Вы успешно вошли в систему',
      life: 3000
    });
    
    // Получаем сохраненный путь или параметр redirect из URL
    const redirectPath = router.currentRoute.value.query.redirect || localStorage.getItem('redirectPath') || '/customers';
    
    // Очищаем сохраненный путь
    localStorage.removeItem('redirectPath');
    
    // Перенаправляем пользователя
    router.push(redirectPath);
  } catch (error) {
    console.error('Ошибка авторизации:', error);
    console.error('Детали ошибки:', error.response?.data);
    errorMessage.value = error.response?.data?.detail || 'Ошибка авторизации';
    toast.add({
      severity: 'error',
      summary: 'Ошибка',
      detail: error.response?.data?.detail || 'Неверное имя пользователя или пароль',
      life: 5000
    });
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.max-w-30rem {
  max-width: 30rem;
}

:deep(.p-password) {
  width: 100%;
}

:deep(.p-password-input) {
  width: 100%;
}

:deep(.p-inputtext) {
  width: 100%;
}

:deep(.p-float-label) {
  width: 100%;
}
</style>
