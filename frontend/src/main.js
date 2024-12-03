import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import PrimeVue from 'primevue/config';
import Lara from '@primevue/themes/lara';
import 'primeicons/primeicons.css'
import './assets/main.css'
import Button from "primevue/button"
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import DatePicker from 'primevue/calendar';
import Message from 'primevue/message';
import Dialog from 'primevue/dialog';
import InputText from 'primevue/inputtext';
import InputMask from 'primevue/inputmask';
import RadioButton from 'primevue/radiobutton';
import ToastService from 'primevue/toastservice';
import Toast from 'primevue/toast';
import Card from 'primevue/card';
import Tag from 'primevue/tag';
import { definePreset } from '@primevue/themes';

const MyPreset = definePreset(Lara, {
    semantic: {
        primary: {
            50: '{purple.50}',
            100: '{purple.100}',
            200: '{purple.200}',
            300: '{purple.300}',
            400: '{purple.400}',
            500: '{purple.500}',
            600: '{purple.600}',
            700: '{purple.700}',
            800: '{purple.800}',
            900: '{purple.900}',
            950: '{purple.950}'
        }
    }
});

const app = createApp(App);
app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: MyPreset,
        options: {
            prefix: 'p',
            darkModeSelector: 'light',
        }
    }
});
app.use(ToastService);
app.component('Prime-Button', Button)
app.component('Prime-DataTable', DataTable)
app.component('Prime-Column', Column)
app.component('Prime-DatePicker', DatePicker)
app.component('Prime-Message', Message)
app.component('Prime-Dialog', Dialog)
app.component('Prime-InputText', InputText)
app.component('Prime-InputMask', InputMask)
app.component('Prime-RadioButton', RadioButton)
app.component('Prime-Toast', Toast)
app.component('Prime-Card', Card)
app.component('Prime-Tag', Tag)
app.mount('#app');
