<template>
  <div class="max-w-[85%] mx-auto">
    <h1 class="text-3xl font-bold text-gray-800 m-4">Финансовая отчетность</h1>
    <div class="card w-full">
      <Prime-Toast />
      
      <!-- Фильтры по датам -->
      <div class="flex gap-4 mb-4">
        <div class="flex flex-col">
          <label>Дата начала</label>
          <Prime-DatePicker 
            v-model="startDate" 
            dateFormat="dd.mm.yy"
            :max="endDate"
            @update:modelValue="validateDates" />
        </div>
        <div class="flex flex-col">
          <label>Дата окончания</label>
          <Prime-DatePicker 
            v-model="endDate" 
            dateFormat="dd.mm.yy"
            :min="startDate"
            @update:modelValue="validateDates" />
        </div>
        <Prime-Button 
          label="Сформировать отчет" 
          @click="generateReport" 
          class="self-end"
          :disabled="!isValidDateRange" />
      </div>
      
      <!-- Общая статистика -->
      <div class="grid grid-cols-4 gap-4 mb-4">
        <Prime-Card>
          <template #title>Выручка ₽</template>
          <template #content>
            <div class="text-2xl font-bold text-blue-600">{{ totalPayments }}</div>
          </template>
        </Prime-Card>
        <Prime-Card>
          <template #title>Выплата зарплат ₽</template>
          <template #content>
            <div class="text-2xl font-bold text-red-600">{{ totalSalaries }}</div>
          </template>
        </Prime-Card>
        <Prime-Card>
          <template #title>Прибыль ₽</template>
          <template #content>
            <div class="text-2xl font-bold text-green-600">{{ totalProfit }}</div>
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

      <!-- График отношения выручки и расходов -->
      <Prime-Card class="mb-4">
        <template #title>Отношение выручки и расходов ₽</template>
        <template #content>
          <Chart type="doughnut" :data="DoughnutChartData" :options="chartOptions" :plugins="[ChartDataLabels, centerTextPlugin]" class="w-full h-[400px]" />
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
          <Prime-DataTable showGridlines :value="teacherStats" paginator :rows="15" removableSort class="w-full">
            <Prime-Column field="name" header="Преподаватель" sortable></Prime-Column>
            <Prime-Column field="total_revenue" header="Доход от курсов ₽" sortable style="text-align: right">
              <template #body="slotProps">
                {{ formatNumber(slotProps.data.total_revenue) }}
              </template>
            </Prime-Column>
            <Prime-Column field="total_salary" header="Зарплата ₽" sortable style="text-align: right">
              <template #body="slotProps">
                {{ formatNumber(slotProps.data.total_salary) }}
              </template>
            </Prime-Column>
            <Prime-Column field="efficiency" header="% от дохода" sortable style="text-align: right">
              <template #body="slotProps">
                <Prime-Tag :severity="getEfficiencySeverity(slotProps.data.efficiency)">
                  {{ slotProps.data.efficiency.toFixed(2) }}
                </Prime-Tag>
              </template>
            </Prime-Column>
            <Prime-Column field="total_students" header="Студентов" sortable style="text-align: right"></Prime-Column>
            <Prime-Column field="courses_count" header="Курсов" sortable style="text-align: right"></Prime-Column>
          </Prime-DataTable>
        </template>
      </Prime-Card>

      <!-- Детальная таблица -->
      <Prime-Card class="mb-4">
        <template #title>Детальная таблица по платежам</template>
        <template #content>
          <Prime-DataTable showGridlines :value="detailedData" paginator :rows="10" class="w-full">
          <Prime-Column field="date" header="Дата" sortable style="width: 15%"></Prime-Column>
          <Prime-Column field="course" header="Курс" sortable style="width: 30%"></Prime-Column>
          <Prime-Column field="customer" header="Плательщик" sortable style="width: 30%"></Prime-Column>
          <Prime-Column field="amount" header="Сумма ₽" sortable style="width: 12.5%; text-align: right">
            <template #body="slotProps">
              {{ formatNumber(slotProps.data.amount) }}
            </template>
          </Prime-Column>
          <Prime-Column field="status" header="Статус" sortable style="width: 12.5%">
            <template #body="slotProps">
              <Prime-Tag :severity="getStatusSeverity(slotProps.data.status)">
                {{ getStatusLabel(slotProps.data.status) }}
              </Prime-Tag>
            </template>
          </Prime-Column>
        </Prime-DataTable>
        </template>
      </Prime-Card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import api from '@/services/api.js';
import { useToast } from 'primevue/usetoast';
import Chart from 'primevue/chart';
import ChartDataLabels from 'chartjs-plugin-datalabels';

const toast = useToast();
const startDate = ref(null);
const endDate = ref(null);
const totalPayments = ref(0);
const totalSalaries = ref(0);
const totalProfit = ref(0);
const paidPercentage = ref(0);
const detailedData = ref([]);
const teacherStats = ref([]);
const isValidDateRange = ref(true);

watch(teacherStats, (newValue) => {
  console.log('Teacher stats changed:', newValue);
}, { deep: true });

// Данные для графиков
const DoughnutChartData = ref({
  datasets: [{
    data: [0, 0],
    backgroundColor: [
      '#22C55E',  // Зеленый для прибыли
      '#EF4444',  // Красный для расходов
    ]
  }]
});

const monthlyData = ref({
  labels: [],
  datasets: [
    {
      label: 'Выручка',
      data: [],
      borderColor: '#3B82F6',
      backgroundColor: '#3B82F6',
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
      borderColor: '#22C55E',
      backgroundColor: '#22C55E',
      tension: 0.4
    }
  ]
});

// Настройки для графиков
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom'
    },
    title: {
      display: true,
      text: ''
    },
    tooltip: {
      callbacks: {
        label: function(context) {
          let label = context.label || '';
          if (label) {
            label += ': ';
          }
          if (context.parsed !== null) {
            label += new Intl.NumberFormat('ru-RU', {
              style: 'decimal',
              minimumFractionDigits: 0,
              maximumFractionDigits: 0
            }).format(context.parsed);
          }
          return label;
        }
      }
    },
    datalabels: {
      display: true,
      color: '#fff',
      font: {
        weight: 'bold'
      },
      formatter: function(value) {
        return new Intl.NumberFormat('ru-RU', {
          style: 'decimal',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0
        }).format(value);
      }
    }
  }
});

const monthlyOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom '
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

// Плагин для центрального текста
const centerTextPlugin = {
  id: 'centerText',
  afterDraw: (chart) => {
    const { ctx, chartArea: { left, top, width, height } } = chart;

    ctx.save();
    
    // Рисуем подпись "Выручка"
    ctx.font = 'bold 14px Arial';
    ctx.fillStyle = '#3B82F6';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Выручка', width / 2 + left, height / 2 + top - 15);

    // Рисуем значение
    ctx.font = 'bold 16px Arial';
    ctx.fillStyle = '#3B82F6';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const text = new Intl.NumberFormat('ru-RU', {
      style: 'decimal',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(totalPayments.value);
    ctx.fillText(text, width / 2 + left, height / 2 + top + 15);
    
    ctx.restore();
  }
};

function formatNumber(value) {
  return new Intl.NumberFormat('ru-RU', { 
    style: 'decimal',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(value);
}

function getEfficiencySeverity(efficiency) {
  if (efficiency <= 30) return 'success';
  if (efficiency <= 50) return 'warning';
  return 'danger';
}

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

    const data = response.data;

    if (!data.detailed_data.length && !data.teacher_stats.length) {
      toast.add({ 
        severity: 'info', 
        summary: 'Нет данных', 
        detail: 'За выбранный период нет данных для отображения', 
        life: 7000 
      });
      return;
    }

    // Обновляем данные
    totalPayments.value = data.total_payments || 0;
    totalSalaries.value = data.total_teacher_salaries || 0;
    totalProfit.value = data.total_profit || 0;
    teacherStats.value = data.teacher_stats || [];
    
    console.log('Teacher stats:', teacherStats.value);

    // Вычисляем процент оплаченных платежей
    const paidPayments = data.detailed_data?.filter(p => p.status === 'paid').length || 0;
    const totalPaymentsCount = data.detailed_data?.length || 0;
    paidPercentage.value = totalPaymentsCount > 0 ? Math.round((paidPayments / totalPaymentsCount) * 100) : 0;
    
    // Обновляем график доходов и расходов
    DoughnutChartData.value = {
      labels: ['Прибыль', 'Расходы на зарплаты преподавателей'],
      datasets: [{
        ...DoughnutChartData.value.datasets[0],
        data: [
          response.data.total_profit,
          response.data.total_teacher_salaries
        ]
      }]
    };

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
    'pending': 'Оплачивается',
    'failed': 'Платёж не прошел',
    'refunded': 'Оформлен возврат'
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

function validateDates() {
  if (startDate.value && endDate.value) {
    const fourWeeksInMs = 28 * 24 * 60 * 60 * 1000; // 28 дней в миллисекундах
    const timeDiff = endDate.value - startDate.value;
    
    isValidDateRange.value = startDate.value < endDate.value && timeDiff >= fourWeeksInMs;
    
    if (!isValidDateRange.value) {
      if (startDate.value >= endDate.value) {
        toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Дата начала должна быть меньше даты окончания', life: 3000 });
      } else {
        toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Минимальный период отчёта - 4 недели', life: 3000 });
      }
    }
  }
}

onMounted(() => {
  const now = new Date();
  endDate.value = now;
  // Устанавливаем начальную дату на 4 недели раньше конечной
  startDate.value = new Date(now.getTime() - (28 * 24 * 60 * 60 * 1000));
  validateDates();
});
</script>

<style>
.p-datatable-column-header-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}
</style>