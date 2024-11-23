<template>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import api from '@/services/api.js';

export default {
    data() {
        return {
            message: '',  // Инициализация переменной message
        };
    },
    mounted() {
        // Получаем данные с API при монтировании компонента
        api.get('example/')
            .then((response) => {
                this.message = response.data.message
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                this.message = "Error loading message";
            });
    },
};
</script>

<style scoped>
h1 {
    font-size: 2rem;
    color: #333;
}
</style>
