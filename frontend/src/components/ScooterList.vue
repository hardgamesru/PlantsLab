<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Список самокатов</h2>

    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error" class="text-red-600">Ошибка: {{ error }}</div>
    <div v-else>
      <ul class="space-y-2">
        <li v-for="scooter in scooters" :key="scooter.id" class="border p-2 rounded shadow">
          <strong>ID:</strong> {{ scooter.id }} |
          <strong>Заряд:</strong> {{ scooter.battery_level }}% |
          <strong>Неисправен:</strong> {{ scooter.is_broken ? 'Да' : 'Нет' }} |
          <strong>Станция:</strong> {{ scooter.station_id ?? 'Не привязан' }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const scooters = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await fetch('/api/')
    if (!res.ok) throw new Error(`Ошибка ${res.status}`)
    scooters.value = await res.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* можно стилизовать дополнительно */
</style>
