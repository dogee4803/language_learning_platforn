<template>
      <h1>Учёт покупателей</h1>
      <Prime-Button label="Добавить" />
    <div class="card">
        <Prime-DataTable :value="customers" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" tableStyle="max-width: 75rem">
            <Prime-Column field="id" header="ID" style="width: 25%"></Prime-Column>
            <Prime-Column field="last_name" header="Фамилия" style="width: 25%"></Prime-Column>
            <Prime-Column field="gender" header="Пол" style="width: 25%"></Prime-Column>
            <Prime-Column field="phone_number" header="Телефон" style="width: 25%"></Prime-Column>
            <Prime-Column field="birth_date" header="ДР" style="width: 25%"></Prime-Column>
        </Prime-DataTable>
    </div>
  </template>
  
  <script setup>
  import api from '@/services/api.js';
  import { ref, onMounted } from 'vue';

  const customers = ref([]);

  // Загружаем данные из API при монтировании компонента
  const fetchCustomers = async () => {
      try {
        const response = await api.get("customers/");
        customers.value = response.data; // Предполагается, что API возвращает массив покупателей
      } catch (error) {
        console.error("Ошибка загрузки покупателей:", error);
      }
    };

  // Вызываем функцию загрузки данных
  onMounted(fetchCustomers);

  console.log(customers)

  </script>
  