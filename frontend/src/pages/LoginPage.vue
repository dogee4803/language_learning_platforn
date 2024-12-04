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
        type="button"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'primevue/usetoast';
import { useAuth } from '@/services/auth';
import api from '@/services/api';

const router = useRouter();
const toast = useToast();
const { setAuthenticated } = useAuth();

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
  errors.value = {};
  errorMessage.value = '';
  
  try {
    const response = await api.post('auth/login/', {
      username: username.value,
      password: password.value
    });
    
    localStorage.setItem('token', response.data.token);
    setAuthenticated(true);
    
    toast.add({
      severity: 'success',
      summary: 'Успешно',
      detail: 'Вы вошли в систему',
      life: 3000
    });
    
    router.push('/');
  } catch (error) {
    console.error('Ошибка при входе:', error);
    if (error.response?.data) {
      if (typeof error.response.data === 'object') {
        errors.value = error.response.data;
      } else {
        errorMessage.value = error.response.data;
      }
    } else {
      errorMessage.value = 'Произошла ошибка при входе в систему';
    }
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
