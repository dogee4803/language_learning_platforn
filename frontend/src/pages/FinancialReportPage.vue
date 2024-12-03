<template>
  <div class="max-w-[85%] mx-auto">
    <h1 class="text-3xl font-bold text-gray-800 m-4">Финансовая отчетность</h1>
    <div class="card w-full">
      <Prime-Toast />
      
      <!-- Фильтры по датам -->
      <div class="flex gap-4 mb-4">
        <div class="flex flex-col">
          <label>Дата начала</label>
          <Prime-DatePicker v-model="startDate" dateFormat="dd.mm.yy" />
        </div>
        <div class="flex flex-col">
          <label>Дата окончания</label>
          <Prime-DatePicker v-model="endDate" dateFormat="dd.mm.yy" />
        </div>
        <Prime-Button label="Сформировать отчет" @click="generateReport" class="self-end" />
      </div>

      <!-- Общая статистика -->
      <div class="grid grid-cols-4 gap-4 mb-4">
        <Prime-Card>
          <template #title>Общая сумма оплат</template>
          <template #content>
            <div class="text-2xl font-bold text-blue-600">{{ totalPayments }} ₽</div>
          </template>
        </Prime-Card>
        <Prime-Card>
          <template #title>Зарплаты преподавателей</template>
          <template #content>
            <div class="text-2xl font-bold text-red-600">{{ totalSalaries }} ₽</div>
          </template>
        </Prime-Card>
        <Prime-Card>
          <template #title>Общая прибыль</template>
          <template #content>
            <div class="text-2xl font-bold" :class="{'text-green-600': totalProfit >= 0, 'text-red-600': totalProfit < 0}">
              {{ totalProfit }} ₽
            </div>
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
        <template #title>Статистика по месяцам</template>
        <template #content>
          <Chart type="line" :data="monthlyData" :options="monthlyOptions" class="w-full h-[400px]" />
        </template>
      </Prime-Card>

      <!-- Зарплаты преподавателей -->
      <Prime-Card class="mb-4">
        <template #title>Статистика по преподавателям</template>
        <template #content>
          <Prime-DataTable :value="teacherStats" paginator :rows="5" class="w-full">
            <Prime-Column field="name" header="Преподаватель" sortable></Prime-Column>
            <Prime-Column field="total_revenue" header="Доход от курсов" sortable>
              <template #body="slotProps">
                {{ formatCurrency(slotProps.data.total_revenue) }}
              </template>
            </Prime-Column>
            <Prime-Column field="total_salary" header="Зарплата" sortable>
              <template #body="slotProps">
                {{ formatCurrency(slotProps.data.total_salary) }}
              </template>
            </Prime-Column>
            <Prime-Column field="efficiency" header="% от дохода" sortable>
              <template #body="slotProps">
                <Prime-Tag :severity="getEfficiencySeverity(slotProps.data.efficiency)">
                  {{ slotProps.data.efficiency }}%
                </Prime-Tag>
              </template>
            </Prime-Column>
            <Prime-Column field="total_students" header="Студентов" sortable></Prime-Column>
            <Prime-Column field="courses_count" header="Курсов" sortable></Prime-Column>
          </Prime-DataTable>
        </template>
      </Prime-Card>

      <!-- Детальная таблица -->
      <Prime-DataTable :value="detailedData" paginator :rows="10" class="w-full">
        <Prime-Column field="date" header="Дата" sortable></Prime-Column>
        <Prime-Column field="course" header="Курс" sortable></Prime-Column>
        <Prime-Column field="language" header="Язык" sortable></Prime-Column>
        <Prime-Column field="teacher" header="Преподаватель" sortable></Prime-Column>
        <Prime-Column field="amount" header="Сумма" sortable>
          <template #body="slotProps">
            {{ slotProps.data.amount }} ₽
          </template>
        </Prime-Column>
        <Prime-Column field="status" header="Статус" sortable>
          <template #body="slotProps">
            <Prime-Tag :severity="getStatusSeverity(slotProps.data.status)">
              {{ getStatusLabel(slotProps.data.status) }}
            </Prime-Tag>
          </template>
        </Prime-Column>
      </Prime-DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import api from '@/services/api.js';
import Chart from 'primevue/chart';

const startDate = ref(null);
const endDate = ref(null);
const totalPayments = ref(0);
const totalSalaries = ref(0);
const totalProfit = ref(0);
const paidPercentage = ref(0);
const detailedData = ref([]);
const teacherStats = ref([]);

watch(teacherStats, (newValue) => {
  console.log('Teacher stats changed:', newValue);
}, { deep: true });

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
  datasets: [
    {
      label: 'Доходы',
      data: [],
      borderColor: '#22C55E',
      backgroundColor: '#22C55E',
      tension: 0.4
    },
    {
      label: 'Расходы',
      data: [],
      borderColor: '#EF4444',
      backgroundColor: '#EF4444',
      tension: 0.4
    },
    {
      label: 'Прибыль',
      data: [],
      borderColor: '#3B82F6',
      backgroundColor: '#3B82F6',
      tension: 0.4
    }
  ]
});


function formatCurrency(value) {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value);
}

function getEfficiencySeverity(efficiency) {
  if (efficiency <= 30) return 'success';
  if (efficiency <= 50) return 'warning';
  return 'danger';
}

const chartOptions = ref({
  plugins: {
    legend: {
      position: 'bottom'
    }
  },
  responsive: true,
  maintainAspectRatio: false
});

const monthlyOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top'
    },
    title: {
      display: true,
      text: 'Статистика по месяцам'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: {
        callback: function(value) {
          return value + ' ₽';
        }
      }
    }
  }
});

async function generateReport() {
  if (!startDate.value || !endDate.value) {
    console.log('Dates not selected');
    return;
  }

  try {
    console.log('Generating report with dates:', {
      start: startDate.value.toISOString().split('T')[0],
      end: endDate.value.toISOString().split('T')[0]
    });

    const response = await api.get('financial-report/', {
      params: {
        start_date: startDate.value.toISOString().split('T')[0],
        end_date: endDate.value.toISOString().split('T')[0]
      }
    });

    console.log('API Response:', response.data);

    if (response.data.error) {
      console.error('API Error:', response.data.error);
      return;
    }

    // Обновляем данные
    totalPayments.value = response.data.total_payments || 0;
    totalSalaries.value = response.data.total_teacher_salaries || 0;
    totalProfit.value = response.data.total_profit || 0;
    teacherStats.value = response.data.teacher_stats || [];
    
    console.log('Teacher stats:', teacherStats.value);

    // Вычисляем процент оплаченных платежей
    const paidPayments = response.data.detailed_data?.filter(p => p.status === 'paid').length || 0;
    const totalPaymentsCount = response.data.detailed_data?.length || 0;
    paidPercentage.value = totalPaymentsCount > 0 ? Math.round((paidPayments / totalPaymentsCount) * 100) : 0;
    
    // Обновляем график по языкам
    if (response.data.language_stats?.length > 0) {
      languageData.value = {
        ...languageData.value,
        labels: response.data.language_stats.map(item => item.language),
        datasets: [{
          ...languageData.value.datasets[0],
          data: response.data.language_stats.map(item => item.total)
        }]
      };
    }

    // Обновляем график по месяцам
    if (response.data.monthly_stats?.length > 0) {
      monthlyData.value = {
        labels: response.data.monthly_stats.map(item => item.month),
        datasets: [
          {
            ...monthlyData.value.datasets[0],
            data: response.data.monthly_stats.map(item => item.revenue)
          },
          {
            ...monthlyData.value.datasets[1],
            data: response.data.monthly_stats.map(item => item.expenses)
          },
          {
            ...monthlyData.value.datasets[2],
            data: response.data.monthly_stats.map(item => item.profit)
          }
        ]
      };
    }

    // Обновляем детальную таблицу
    detailedData.value = response.data.detailed_data || [];
  } catch (error) {
    console.error('Error generating report:', error);
    console.error('Error details:', error.response?.data);
  }
}

function getStatusLabel(status) {
  const labels = {
    'paid': 'Оплачено',
    'pending': 'Ожидает',
    'failed': 'Ошибка',
    'refunded': 'Возврат'
  };
  return labels[status] || status;
}

function getStatusSeverity(status) {
  const severities = {
    'paid': 'success',
    'pending': 'warning',
    'failed': 'danger',
    'refunded': 'info'
  };
  return severities[status] || 'warning';
}

onMounted(() => {
  // Устанавливаем начальные даты (например, текущий месяц)
  const now = new Date();
  endDate.value = now;
  startDate.value = new Date(now.getFullYear(), now.getMonth(), 1);
  generateReport();
});
</script>
