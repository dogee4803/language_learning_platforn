<template>
    <nav class="card">
        <Menubar :model="items" />
    </nav>
</template>

<script setup>
import Menubar from 'primevue/menubar';
import { ref } from "vue";

const items = ref([
    {
        label: 'Покупатели',
        icon: 'pi pi-users'
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
    }
]);
</script>