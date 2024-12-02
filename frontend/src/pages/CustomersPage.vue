<template>
      <h1>Учёт покупателей</h1>
      <Prime-Button label="Добавить" />
    <div class="card">
        <Prime-DataTable :value="customers" paginator :rows="5" :rowsPerPageOptions="[5, 10, 20, 50]" removableSort tableStyle="max-width: 75rem">
            <Prime-Column field="id" header="ID" sortable style="width: 5%"></Prime-Column>
            <Prime-Column field="last_name" header="Фамилия" sortable style="width: 20%"></Prime-Column>
            <Prime-Column field="first_name" header="Имя" sortable style="width: 20%"></Prime-Column>
            <Prime-Column field="middle_name" header="Отчество" sortable style="width: 20%"></Prime-Column>
            <Prime-Column field="sex" header="Пол" sortable style="width: 5%">
                <template #body="slotProps">
                    {{ slotProps.data.sex ? 'М' : 'Ж' }}
                </template>
            </Prime-Column>
            <Prime-Column field="phone_number" header="Телефон" sortable style="width: 20%"></Prime-Column>
            <Prime-Column field="birth_date" header="Дата рождения" sortable style="width: 10%"></Prime-Column>
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