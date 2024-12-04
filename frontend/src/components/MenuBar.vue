<template>
    <nav v-if="isLoggedIn">
        <Menubar :model="items" class="flex justify-content-between">
            <template #end>
                <Prime-Button 
                    icon="pi pi-sign-out" 
                    label="Выйти" 
                    severity="secondary"
                    text
                    @click="logout"
                />
            </template>
        </Menubar>
    </nav>
</template>

<script setup>
import Menubar from 'primevue/menubar';
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { useToast } from 'primevue/usetoast';
import api from '@/services/api';

const router = useRouter();
const toast = useToast();
const isLoggedIn = ref(!!localStorage.getItem('token'));

// Слушаем изменения в localStorage
const handleStorageChange = () => {
    isLoggedIn.value = !!localStorage.getItem('token');
};

onMounted(() => {
    window.addEventListener('storage', handleStorageChange);
    // Проверяем при монтировании
    isLoggedIn.value = !!localStorage.getItem('token');
});

onUnmounted(() => {
    window.removeEventListener('storage', handleStorageChange);
});

const logout = async () => {
    try {
        await api.post('auth/logout/');
        
        // Удаляем токен
        localStorage.removeItem('token');
        isLoggedIn.value = false;
        
        // Удаляем заголовок авторизации
        delete api.defaults.headers.common['Authorization'];
        
        toast.add({
            severity: 'success',
            summary: 'Успешно',
            detail: 'Вы вышли из системы',
            life: 3000
        });
        
        // Перенаправляем на страницу входа
        router.push('/login');
    } catch (error) {
        console.error('Ошибка при выходе:', error);
        toast.add({
            severity: 'error',
            summary: 'Ошибка',
            detail: 'Не удалось выйти из системы',
            life: 5000
        });
    }
};

const items = ref([
    {
        label: 'Покупатели',
        icon: 'pi pi-users',
        command: () => router.push('/customers')
    },
    {
        label: 'Преподаватели',
        icon: 'pi pi-users'
    },
    {
        label: 'Курсы',
        icon: 'pi pi-book',
    },
    {
        label: 'Языки',
        icon: 'pi pi-globe',
    },
    {
        label: 'Отчёты',
        icon: 'pi pi-chart-line',
        items: [
            {
                label: 'Финансовый отчёт',
                icon: 'pi pi-dollar',
                command: () => router.push('/financial-report')
            },
            {
                label: 'Успеваемость',
                icon: 'pi pi-trophy'
            },
            {
                label: 'Статистика курсов',
                icon: 'pi pi-chart-bar'
            }
        ]
    }
]);
</script>

<style scoped>
:deep(.p-menubar) {
    padding: 0.5rem 1rem;
}

:deep(.p-menubar-end) {
    margin-left: auto;
}
</style>