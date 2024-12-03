<template>
  <div class="max-w-[85%] mx-auto">
    <h1 class="text-3xl font-bold text-gray-800 m-4">Учёт покупателей</h1>
    <div class="card w-full">
      <Prime-Toast />
      
      <!-- Сообщения об ошибках -->
      <div v-if="errorMessage" class="mb-3">
        <Prime-Message severity="error">
          <div v-if="typeof errorMessage === 'string'">{{ errorMessage }}</div>
          <div v-else>
            <div v-for="(error, field) in errorMessage" :key="field">
              <strong>{{ field }}:</strong> {{ Array.isArray(error) ? error.join(', ') : error }}
            </div>
          </div>
        </Prime-Message>
      </div>

      <Prime-DataTable 
      showGridlines
      ref="dt" 
      :value="customers" 
      paginator 
      :rows="5"
      :rowsPerPageOptions="[5, 10, 20, 50]" 
      dataKey="id" 
      removableSort
      v-model:editingRows="editingRows" 
      editMode="row"
      @row-edit-init="onRowEditInit"
      @cell-edit-complete="onCellEditComplete"
      @row-edit-save="onRowEditSave"
      @row-edit-cancel="onRowEditCancel"
      class="w-full"
      tableStyle="min-width: 100%">
        <template #header>
          <div class="flex justify-between">
            <Prime-Button label="Добавить покупателя" icon="pi pi-plus" @click="showDialog = true" />
            <Prime-Button icon="pi pi-external-link" label="Export" @click="exportCSV($event)" />
          </div>
        </template>
        <Prime-Column field="id" header="ID" sortable style="width: 5%; text-align: right"></Prime-Column>
        <Prime-Column field="last_name" header="Фамилия" sortable style="width: 19%">
          <template #editor="{ data, field }">
            <Prime-InputText v-model="editingData[field]" @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" class="w-full" :class="{ 'p-invalid': validationErrors.last_name }" />
            <small v-if="validationErrors.last_name">{{ validationErrors.last_name }}</small>
            <small v-if="editErrors.last_name">{{ editErrors.last_name }}</small>
          </template>
        </Prime-Column>
        <Prime-Column field="first_name" header="Имя" sortable style="width: 19%">
          <template #editor="{ data, field }">
            <Prime-InputText v-model="editingData[field]" @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" class="w-full" :class="{ 'p-invalid': validationErrors.first_name }" />
            <small v-if="validationErrors.first_name">{{ validationErrors.first_name }}</small>
            <small v-if="editErrors.first_name">{{ editErrors.first_name }}</small>
          </template>
        </Prime-Column>
        <Prime-Column field="middle_name" header="Отчество" sortable style="width: 19%">
          <template #editor="{ data, field }">
            <Prime-InputText v-model="editingData[field]" @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" class="w-full" :class="{ 'p-invalid': validationErrors.middle_name }" />
            <small v-if="validationErrors.middle_name" class="p-error">{{ validationErrors.middle_name }}</small>
            <small v-if="editErrors.middle_name">{{ editErrors.middle_name }}</small>
          </template>
        </Prime-Column>
        <Prime-Column field="sex" header="Пол" sortable style="width: 5%">
          <template #body="slotProps">
            {{ slotProps.data.sex === true ? 'М' : 'Ж' }}
          </template>
          <template #editor="{ data }">
            <div class="flex align-items-center">
              <Prime-RadioButton v-model="editingData.sex" :value="true" inputId="sex1_edit" name="sex_edit" 
                @change="onCellEditComplete({ data, field: 'sex', newValue: true })" />
              <label for="sex1_edit" class="ml-2 mr-4">М</label>
              <Prime-RadioButton v-model="editingData.sex" :value="false" inputId="sex2_edit" name="sex_edit"
                @change="onCellEditComplete({ data, field: 'sex', newValue: false })" />
              <label for="sex2_edit" class="ml-2">Ж</label>
            </div>
            <small v-if="editErrors.sex">{{ editErrors.sex }}</small>
          </template>
        </Prime-Column>
        <Prime-Column field="phone_number" header="Телефон" sortable style="width: 18%; text-align: left">
          <template #editor="{ data, field }">
            <Prime-InputMask v-model="editingData[field]" mask="+9 (999) 999 99-99" placeholder="+x (xxx) xxx xx-xx" class="w-full"
              @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" />
            <small v-if="editErrors.phone_number">{{ editErrors.phone_number }}</small>
          </template>
        </Prime-Column>
        <Prime-Column field="birth_date" header="Дата рождения" sortable style="width: 10%; text-align: left">
          <template #editor="{ data, field }">
            <Prime-DatePicker v-model="editingData[field]" dateFormat="dd.mm.yy" class="w-full"
              @update:modelValue="onCellEditComplete({ data, field, newValue: $event })" />
            <small v-if="editErrors.birth_date">{{ editErrors.birth_date }}</small>
          </template>
        </Prime-Column>
        <Prime-Column :rowEditor="true" style="width: 5%; min-width: 4rem"></Prime-Column>
        <Prime-Column style="width: 5%; min-width: 4rem">
          <template #body="{ data }">
            <Prime-Button icon="pi pi-trash" severity="danger" text rounded @click="deleteRow(data)" />
          </template>
        </Prime-Column>
      </Prime-DataTable>

      <Prime-Dialog 
        v-model:visible="showDialog" 
        modal 
        header="Добавить покупателя" 
        :style="{ width: '450px' }"
        class="p-fluid">
        <div class="grid">
          <div class="col-12 mb-2">
            <Prime-InputText v-model="newCustomer.last_name" placeholder="Фамилия" class="w-full" :class="{ 'p-invalid': validationErrors.last_name }" />
            <small v-if="validationErrors.last_name">{{ validationErrors.last_name }}</small>
            <small v-if="errorsAdd.last_name">{{ errorsAdd.last_name }}</small>
          </div>
          <div class="col-12 mb-2">
            <Prime-InputText v-model="newCustomer.first_name" placeholder="Имя" class="w-full" :class="{ 'p-invalid': validationErrors.first_name }" />
            <small v-if="validationErrors.first_name">{{ validationErrors.first_name }}</small>
            <small v-if="errorsAdd.first_name">{{ errorsAdd.first_name }}</small>
          </div>
          <div class="col-12 mb-2">
            <Prime-InputText v-model="newCustomer.middle_name" placeholder="Отчество" class="w-full" :class="{ 'p-invalid': validationErrors.middle_name }" />
            <small v-if="validationErrors.middle_name">{{ validationErrors.middle_name }}</small>
            <small v-if="errorsAdd.middle_name">{{ errorsAdd.middle_name }}</small>
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
            <small v-if="errorsAdd.sex">{{ errorsAdd.sex }}</small>
          </div>
          <div class="col-12 mb-2">
            <Prime-InputMask v-model="newCustomer.phone_number" mask="+9 (999) 999 99-99" placeholder="+x (xxx) xxx xx-xx" class="w-full" />
            <small v-if="errorsAdd.phone_number">{{ errorsAdd.phone_number }}</small>
          </div>
          <div class="col-12 mb-2">
            <Prime-DatePicker v-model="newCustomer.birth_date" placeholder="Дата рождения" class="w-full" dateFormat="dd.mm.yy" />
            <small v-if="errorsAdd.birth_date">{{ errorsAdd.birth_date }}</small>
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
  </div>
</template>

<script setup>
import api from '@/services/api.js';
import { ref, onMounted } from 'vue';
import { useToast } from 'primevue/usetoast';

const toast = useToast();

const customers = ref([]);
const editingRows = ref([]);
const editingData = ref(null); // Для хранения редактируемых данных
const showDialog = ref(false);
const dt = ref();
const errorsAdd = ref({});
const editErrors = ref({});
const errorMessage = ref(null);
const validationErrors = ref({
  last_name: '',
  first_name: '',
  middle_name: ''
});

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
  validationErrors.value = {
    last_name: '',
    first_name: '',
    middle_name: ''
  };
};

const validateCustomer = (customer) => {
    const validationErrors = {};
    
    if (!customer.first_name || /^\s*$/.test(customer.first_name)) {
        validationErrors.first_name = 'Имя обязательно и не должно начинаться с пробела.';
    } else if (!/^[a-zA-Zа-яА-ЯёЁ\s]+$/.test(customer.first_name)) {
        validationErrors.first_name = 'Имя может содержать только буквы.';
    }

    if (!customer.last_name || /^\s*$/.test(customer.last_name)) {
        validationErrors.last_name = 'Фамилия обязательна и не должна начинаться с пробела.';
    } else if (!/^[a-zA-Zа-яА-ЯёЁ\s]+$/.test(customer.last_name)) {
        validationErrors.last_name = 'Фамилия может содержать только буквы.';
    }

    if (customer.middle_name) {  // Проверяем отчество только если оно есть
        if (/^\s*$/.test(customer.middle_name)) {
            validationErrors.middle_name = 'Отчество не должно начинаться с пробела.';
        } else if (!/^[a-zA-Zа-яА-ЯёЁ\s]+$/.test(customer.middle_name)) {
            validationErrors.middle_name = 'Отчество может содержать только буквы.';
        }
    }

    if (customer.phone_number === null || customer.phone_number === '') {
        validationErrors.phone_number = 'Телефон обязателен.';
    }

    if (!customer.birth_date) {
        validationErrors.birth_date = 'Дата рождения обязательна.';
    } else {
        const birthDate = new Date(customer.birth_date);
        const now = new Date();
        if (birthDate > now) {
            validationErrors.birth_date = 'Дата рождения не может быть в будущем.';
        }
    }

    return validationErrors;
};

const fetchCustomers = async () => {
  try {
    const response = await api.get("customers/");
    customers.value = response.data;
    errorMessage.value = null;
  } catch (error) {
    console.error("Ошибка загрузки покупателей:", error);
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Не удалось загрузить список покупателей' });
    showErrorDetails(error);
  }
};

const addCustomer = async () => {
    const errors = validateCustomer(newCustomer.value);
    if (Object.keys(errors).length > 0) {
        errorsAdd.value = errors;
        toast.add({
            severity: 'error',
            summary: 'Ошибка валидации',
            detail: 'Пожалуйста, исправьте ошибки в форме',
            life: 5000
        });
        return;
    }

    try {
        const customerData = formatCustomerForSave(newCustomer.value);
        console.log('Отправляемые данные:', customerData);
        const response = await api.post('customers/', customerData);
        customers.value.push(response.data);
        toast.add({
            severity: 'success',
            summary: 'Успешно',
            detail: 'Покупатель успешно добавлен',
            life: 3000
        });
        showDialog.value = false;
        newCustomer.value = { sex: true };
        errorsAdd.value = {};
        errorMessage.value = null;
    } catch (error) {
        console.error("Ошибка добавления покупателя:", error);
        toast.add({
            severity: 'error',
            summary: 'Ошибка',
            detail: error.response?.data?.detail || 'Не удалось добавить покупателя',
            life: 5000
        });
        if (error.response?.data) {
            errorsAdd.value = error.response.data;
        }
    }
};

const deleteRow = async (data) => {
  try {
    await api.delete(`customers/${data.id}/`);
    customers.value = customers.value.filter((customer) => customer.id !== data.id);
    toast.add({ severity: 'success', summary: 'Успех', detail: 'Покупатель удален', life: 3000 });
    errorMessage.value = null;
  } catch (error) {
    console.error("Ошибка удаления покупателя:", error);
    toast.add({ severity: 'error', summary: 'Ошибка', detail: 'Не удалось удалить покупателя', life: 5000 });
    showErrorDetails(error);
  }
};

const onRowEditInit = (event) => {
  // Создаем копию данных для редактирования
  editingData.value = { ...event.data };
  console.log('Начало редактирования:', editingData.value);
};

const onCellEditComplete = ({ data, field, newValue }) => {
  editingData.value = { ...data, [field]: newValue };
};

const formatCustomerForSave = (customer) => {
  return {
    ...customer,
    birth_date: customer.birth_date ? new Date(customer.birth_date).toISOString().split('T')[0] : null
  };
};

const onRowEditSave = async () => {
    if (!editingData.value) {
        console.error('Нет данных для обновления');
        return;
    }

    const errors = validateCustomer(editingData.value);
    if (Object.keys(errors).length > 0) {
        editErrors.value = errors;
        toast.add({
            severity: 'error',
            summary: 'Ошибка валидации',
            detail: 'Пожалуйста, исправьте ошибки в форме',
            life: 5000
        });
        return;
    }

    try {
        const customerData = formatCustomerForSave(editingData.value);
        const response = await api.put(`customers/${customerData.id}/`, customerData);
        
        // Обновляем данные в таблице
        const index = customers.value.findIndex(item => item.id === customerData.id);
        if (index !== -1) {
            customers.value[index] = response.data;
        }
        
        toast.add({
            severity: 'success',
            summary: 'Успешно',
            detail: 'Данные покупателя обновлены',
            life: 3000
        });
        
        editErrors.value = {};
        editingData.value = null;
    } catch (error) {
        console.error("Ошибка обновления:", error);
        toast.add({
            severity: 'error',
            summary: 'Ошибка',
            detail: error.response?.data?.detail || 'Не удалось обновить данные',
            life: 5000
        });
        if (error.response?.data) {
            editErrors.value = error.response.data;
        }
    }
};

const onRowEditCancel = () => {
  console.log('Отмена редактирования');
  editErrors.value = {};
  editingData.value = null;
};

const exportCSV = () => {
  dt.value.exportCSV();
};

const showErrorDetails = (error) => {
  if (error.response?.data) {
    errorMessage.value = error.response.data;
  } else {
    errorMessage.value = error.message || 'Произошла неизвестная ошибка';
  }
};

onMounted(fetchCustomers);
</script>

<style>
.p-datatable-column-header-content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}
</style>