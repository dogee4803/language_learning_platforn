<template>
  <h1>Учёт покупателей</h1>
  <div class="card">
    <Prime-DataTable 
    ref="dt" 
    :value="customers" 
    paginator 
    :rows="5" 
    :rowsPerPageOptions="[5, 10, 20, 50]" 
    removableSort
    v-model:editingRows="editingRows" 
    editMode="row"
    @row-edit-init="onRowEditInit"
    @cell-edit-complete="onCellEditComplete"
    @row-edit-save="onRowEditSave"
    @row-edit-cancel="onRowEditCancel"
    tableStyle="max-width: 75rem">
      <template #header>
        <div class="flex justify-between pb-4">
          <Prime-Button label="Добавить покупателя" icon="pi pi-plus" @click="showDialog = true" />
          <Prime-Button icon="pi pi-external-link" label="Export" @click="exportCSV($event)" />
        </div>
      </template>
      <Prime-Column field="id" header="ID" sortable style="width: 5%"></Prime-Column>
      <Prime-Column field="last_name" header="Фамилия" sortable style="width: 20%">
        <template #editor="{ data, field }">
          <div class="field">
            <Prime-InputText v-model="editingData[field]" @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" />
            <small class="p-error" v-if="editErrors.last_name">{{ editErrors.last_name }}</small>
          </div>
        </template>
      </Prime-Column>
      <Prime-Column field="first_name" header="Имя" sortable style="width: 20%">
        <template #editor="{ data, field }">
          <div class="field">
            <Prime-InputText v-model="editingData[field]" @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" />
            <small class="p-error" v-if="editErrors.first_name">{{ editErrors.first_name }}</small>
          </div>
        </template>
      </Prime-Column>
      <Prime-Column field="middle_name" header="Отчество" sortable style="width: 20%">
        <template #editor="{ data, field }">
          <div class="field">
            <Prime-InputText v-model="editingData[field]" @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" />
            <small class="p-error" v-if="editErrors.middle_name">{{ editErrors.middle_name }}</small>
          </div>
        </template>
      </Prime-Column>
      <Prime-Column field="sex" header="Пол" sortable style="width: 5%">
        <template #body="slotProps">
          {{ slotProps.data.sex ? 'М' : 'Ж' }}
        </template>
        <template #editor="{ data }">
          <div class="field">
            <div class="flex align-items-center">
              <Prime-RadioButton v-model="editingData.sex" :value="true" inputId="sex1_edit" name="sex_edit" 
                @change="onCellEditComplete({ data, field: 'sex', newValue: true })" />
              <label for="sex1_edit" class="ml-2 mr-4">М</label>
              <Prime-RadioButton v-model="editingData.sex" :value="false" inputId="sex2_edit" name="sex_edit"
                @change="onCellEditComplete({ data, field: 'sex', newValue: false })" />
              <label for="sex2_edit" class="ml-2">Ж</label>
            </div>
            <small class="p-error" v-if="editErrors.sex">{{ editErrors.sex }}</small>
          </div>
        </template>
      </Prime-Column>
      <Prime-Column field="phone_number" header="Телефон" sortable style="width: 20%">
        <template #editor="{ data, field }">
          <div class="field">
            <Prime-InputMask v-model="editingData[field]" mask="+9 (999) 999 99-99" placeholder="+x (xxx) xxx xx-xx" 
              @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" />
            <small class="p-error" v-if="editErrors.phone_number">{{ editErrors.phone_number }}</small>
          </div>
        </template>
      </Prime-Column>
      <Prime-Column field="birth_date" header="Дата рождения" sortable style="width: 10%">
        <template #editor="{ data, field }">
          <div class="field">
            <Prime-DatePicker v-model="editingData[field]" dateFormat="dd.mm.yy" 
              @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" />
            <small class="p-error" v-if="editErrors.birth_date">{{ editErrors.birth_date }}</small>
          </div>
        </template>
      </Prime-Column>
      <Prime-Column :rowEditor="true" style="width: 10%; min-width: 4rem"></Prime-Column>
      <Prime-Column style="width: 10%; min-width: 4rem">
        <template #body="{ data }">
          <Prime-Button icon="pi pi-trash" severity="danger" text rounded @click="deleteRow(data)" />
        </template>
      </Prime-Column>
    </Prime-DataTable>

    <Prime-Dialog header="Добавить покупателя" v-model:visible="showDialog" :modal="true">
      <div class="grid">
        <div class="col-12 mb-2">
          <Prime-InputText v-model="newCustomer.last_name" placeholder="Фамилия" class="w-full" />
          <small class="p-error" v-if="errorsAdd.last_name">{{ errorsAdd.last_name }}</small>
        </div>
        <div class="col-12 mb-2">
          <Prime-InputText v-model="newCustomer.first_name" placeholder="Имя" class="w-full" />
          <small class="p-error" v-if="errorsAdd.first_name">{{ errorsAdd.first_name }}</small>
        </div>
        <div class="col-12 mb-2">
          <Prime-InputText v-model="newCustomer.middle_name" placeholder="Отчество" class="w-full" />
          <small class="p-error" v-if="errorsAdd.middle_name">{{ errorsAdd.middle_name }}</small>
        </div>
        <div class="col-12 mb-2">
          <div class="flex align-items-center">
            <label class="mr-3">Пол:</label>
            <div class="flex align-items-center">
              <Prime-RadioButton v-model="newCustomer.sex" :value="true" inputId="sex1" name="sex" />
              <label for="sex1" class="ml-2 mr-4">М</label>
              <Prime-RadioButton v-model="newCustomer.sex" :value="false" inputId="sex2" name="sex" />
              <label for="sex2" class="ml-2">Ж</label>
            </div>
          </div>
          <small class="p-error" v-if="errorsAdd.sex">{{ errorsAdd.sex }}</small>
        </div>
        <div class="col-12 mb-2">
          <Prime-InputMask v-model="newCustomer.phone_number" mask="+9 (999) 999 99-99" placeholder="+x (xxx) xxx xx-xx" class="w-full" />
          <small class="p-error" v-if="errorsAdd.phone_number">{{ errorsAdd.phone_number }}</small>
        </div>
        <div class="col-12 mb-2">
          <Prime-DatePicker v-model="newCustomer.birth_date" placeholder="Дата рождения" class="w-full" dateFormat="dd.mm.yy" />
          <small class="p-error" v-if="errorsAdd.birth_date">{{ errorsAdd.birth_date }}</small>
        </div>
      </div>

      <div class="flex justify-content-end mt-4">
        <Prime-Button label="Отмена" icon="pi pi-times" @click="closeDialog" class="p-button-text mr-2" />
        <Prime-Button label="Сохранить" icon="pi pi-check" @click="addCustomer" />
      </div>

      <div v-if="errorsAdd.non_field_errors" class="mt-3">
        <Prime-Message severity="error" :closable="false">{{ errorsAdd.non_field_errors }}</Prime-Message>
      </div>
    </Prime-Dialog>
  </div>
</template>

<script setup>
import api from '@/services/api.js';
import { ref, onMounted } from 'vue';

const customers = ref([]);
const editingRows = ref([]);
const editingData = ref(null); // Для хранения редактируемых данных
const showDialog = ref(false);
const dt = ref();
const errorsAdd = ref({});
const editErrors = ref({});

const newCustomer = ref({
  first_name: '',
  last_name: '',
  middle_name: '',
  phone_number: '',
  sex: true,
  birth_date: ''
});

const closeDialog = () => {
  showDialog.value = false;
  newCustomer.value = {
    first_name: '',
    last_name: '',
    middle_name: '',
    phone_number: '',
    sex: true,
    birth_date: ''
  };
  errorsAdd.value = {};
};

const fetchCustomers = async () => {
  try {
    const response = await api.get("customers/");
    customers.value = response.data;
  } catch (error) {
    console.error("Ошибка загрузки покупателей:", error);
  }
};

const addCustomer = async () => {
  try {
    console.log('Отправляемые данные:', newCustomer.value);
    // Форматируем дату в формат YYYY-MM-DD перед отправкой
    const customerData = {
      ...newCustomer.value,
      birth_date: newCustomer.value.birth_date ? new Date(newCustomer.value.birth_date).toISOString().split('T')[0] : null
    };
    const response = await api.post("customers/", customerData);
    customers.value.push(response.data);
    closeDialog();
  } catch (error) {
    console.error("Ошибка добавления покупателя:", error);
    console.error("Детали ошибки:", error.response?.data);
    errorsAdd.value = error.response?.data || { error: 'Ошибка при добавлении покупателя' };
  }
};

const deleteRow = async (data) => {
  try {
    await api.delete(`customers/${data.id}/`);
    customers.value = customers.value.filter((customer) => customer.id !== data.id);
  } catch (error) {
    console.error("Ошибка удаления покупателя:", error);
    console.error("Детали ошибки:", error.response?.data);
  }
};

const onRowEditInit = (event) => {
  // Создаем копию данных для редактирования
  editingData.value = { ...event.data };
  console.log('Начало редактирования:', editingData.value);
};

const onCellEditComplete = (event) => {
  const { data, field, newValue } = event;
  if (editingData.value && editingData.value.id === data.id) {
    editingData.value[field] = newValue;
    console.log('Изменено поле:', field, 'новое значение:', newValue);
  }
};

const onRowEditSave = async (event) => {
  let dataToUpdate;
  try {
    // Используем editingData вместо event.data
    dataToUpdate = editingData.value || event.data;
    console.log('Исходные данные для обновления:', dataToUpdate);
    
    const customerData = formatCustomerData(dataToUpdate);
    console.log('Отформатированные данные:', customerData);
    
    const response = await api.put(`customers/${dataToUpdate.id}/`, customerData);
    // Обновляем данные в таблице данными с сервера
    const index = customers.value.findIndex(customer => customer.id === dataToUpdate.id);
    if (index !== -1) {
      customers.value[index] = response.data;
    }
    editErrors.value = {};
    editingData.value = null; // Очищаем данные редактирования
  } catch (error) {
    console.error("Ошибка сохранения покупателя:", error);
    console.error("Детали ошибки:", error.response?.data);
    editErrors.value = error.response?.data || { error: 'Ошибка при сохранении покупателя' };
    // Восстанавливаем данные с сервера в случае ошибки
    if (dataToUpdate) {
      try {
        const originalCustomer = await api.get(`customers/${dataToUpdate.id}/`);
        const index = customers.value.findIndex(customer => customer.id === dataToUpdate.id);
        if (index !== -1) {
          customers.value[index] = originalCustomer.data;
        }
      } catch (restoreError) {
        console.error("Ошибка при восстановлении данных:", restoreError);
      }
    }
  }
};

const onRowEditCancel = (event) => {
  console.log('Отмена редактирования:', event.data);
  editErrors.value = {};
  editingData.value = null; // Очищаем данные редактирования
};

const exportCSV = () => {
  dt.value.exportCSV();
};

const formatCustomerData = (data) => {
  return {
    ...data,
    birth_date: data.birth_date ? new Date(data.birth_date).toISOString().split('T')[0] : null
  };
};

onMounted(fetchCustomers);
</script>

<style scoped>
.card {
  background: var(--surface-card);
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: var(--card-shadow);
  border-radius: 12px;
}

h1 {
  margin-bottom: 1.5rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.p-error {
  color: var(--red-500);
  font-size: 0.875rem;
  margin-top: 0.25rem;
}

/* Стили для полей с ошибками */
:deep(.p-inputtext.p-invalid) {
  border-color: var(--red-500);
}

:deep(.p-datepicker.p-invalid) {
  border-color: var(--red-500);
}
</style>