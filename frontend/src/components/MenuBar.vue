<template>
    <nav class="card">
        <Menubar :model="items" />
    </nav>
</template>

<script setup>
import Menubar from 'primevue/menubar';
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

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
        label: 'Отчёт: Успеваемость',
        icon: 'pi pi-trophy'
    },
    {
        label: 'Отчёт: Статистика курсов',
        icon: 'pi pi-chart-bar'
    },
    {
        label: 'About',
        icon: 'pi pi-book',
        command: () => router.push('/about')
    }
]);
</script>