<template>
  <div class="max-w-[85%] mx-auto">
    <h1 class="text-3xl font-bold text-gray-800 m-4">Финансовая отчетность</h1>
    <div class="card w-full">
      <Prime-Toast />
      
      <!-- Фильтры по датам -->
      <div class="flex gap-4 mb-4">
        <div class="flex flex-col">
          <label>Дата начала</label>
          <Prime-Calendar v-model="startDate" dateFormat="dd.mm.yy" />
        </div>
        <div class="flex flex-col">
          <label>Дата окончания</label>
          <Prime-Calendar v-model="endDate" dateFormat="dd.mm.yy" />
        </div>
        <Prime-Button label="Сформировать отчет" @click="generateReport" class="self-end" />
      </div>

      <!-- Общая статистика -->
      <div class="grid grid-cols-2 gap-4 mb-4">
        <Prime-Card>
          <template #title>Общая сумма оплат</template>
          <template #content>
            <div class="text-2xl font-bold">{{ totalPayments }} ₽</div>
          </template>
        </Prime-Card>
        <Prime-Card>
          <template #title>Статус оплат</template>
          <template #content>
            <div class="text-lg">
              <div>Оплачено: {{ paidPercentage }}%</div>
              <div>Не оплачено: {{ 100 - paidPercentage }}%</div>
            </div>
          </template>
        </Prime-Card>
      </div>

      <!-- График доходов по языкам -->
      <Prime-Card class="mb-4">
        <template #title>Доходы по языкам обучения</template>
        <template #content>
          <Chart type="pie" :data="languageData" :options="chartOptions" class="w-full h-[400px]" />
        </template>
      </Prime-Card>

      <!-- График статистики по месяцам -->
      <Prime-Card class="mb-4">
        <template #title>Статистика оплат по месяцам</template>
        <template #content>
          <Chart type="line" :data="monthlyData" :options="chartOptions" class="w-full h-[400px]" />
        </template>
      </Prime-Card>

      <!-- Детальная таблица -->
      <Prime-DataTable :value="detailedData" paginator :rows="10" class="w-full">
        <Prime-Column field="date" header="Дата" sortable></Prime-Column>
        <Prime-Column field="course" header="Курс" sortable></Prime-Column>
        <Prime-Column field="language" header="Язык" sortable></Prime-Column>
        <Prime-Column field="amount" header="Сумма" sortable>
          <template #body="slotProps">
            {{ slotProps.data.amount }} ₽
          </template>
        </Prime-Column>
        <Prime-Column field="status" header="Статус" sortable>
          <template #body="slotProps">
            <Prime-Tag :severity="slotProps.data.status ? 'success' : 'danger'">
              {{ slotProps.data.status ? 'Оплачено' : 'Не оплачено' }}
            </Prime-Tag>
          </template>
        </Prime-Column>
      </Prime-DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api.js';
import Chart from 'primevue/chart';

const startDate = ref(null);
const endDate = ref(null);
const totalPayments = ref(0);
const paidPercentage = ref(0);
const detailedData = ref([]);

// Данные для графиков
const languageData = ref({
  labels: [],
  datasets: [{
    data: [],
    backgroundColor: [
      '#FF6384',
      '#36A2EB',
      '#FFCE56',
      '#4BC0C0',
      '#9966FF'
    ]
  }]
});

const monthlyData = ref({
  labels: [],
  datasets: [{
    label: 'Сумма оплат',
    data: [],
    fill: false,
    borderColor: '#42A5F5',
    tension: 0.4
  }]
});

const chartOptions = ref({
  plugins: {
    legend: {
      position: 'bottom'
    }
  },
  responsive: true,
  maintainAspectRatio: false
});

async function generateReport() {
  if (!startDate.value || !endDate.value) {
    return;
  }

  try {
    const response = await api.get('/api/financial-report/', {
      params: {
        start_date: startDate.value.toISOString().split('T')[0],
        end_date: endDate.value.toISOString().split('T')[0]
      }
    });

    // Обновляем данные
    totalPayments.value = response.data.total_payments;
    paidPercentage.value = response.data.paid_percentage;
    
    // Обновляем график по языкам
    languageData.value.labels = response.data.language_stats.map(item => item.language);
    languageData.value.datasets[0].data = response.data.language_stats.map(item => item.amount);

    // Обновляем график по месяцам
    monthlyData.value.labels = response.data.monthly_stats.map(item => item.month);
    monthlyData.value.datasets[0].data = response.data.monthly_stats.map(item => item.amount);

    // Обновляем детальную таблицу
    detailedData.value = response.data.detailed_data;
  } catch (error) {
    console.error('Error generating report:', error);
  }
}

onMounted(() => {
  // Устанавливаем начальные даты (например, текущий месяц)
  const now = new Date();
  endDate.value = now;
  startDate.value = new Date(now.getFullYear(), now.getMonth(), 1);
  generateReport();
});
</script>
