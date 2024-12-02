<template>
    <nav>
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
        label: 'Отчёты',
        icon: 'pi pi-chart-line',
        items: [
            {
                label: 'Финансовый отчет',
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
    },
    {
        label: 'About',
        icon: 'pi pi-book',
        command: () => router.push('/about')
    }
]);
</script>