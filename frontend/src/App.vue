<template>
  <main class="p-4 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">🚦 Симуляция самокатов</h1>

    <div class="space-x-3 mb-6">
      <button
        @click="start"
        :disabled="running"
        class="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded"
      >Старт</button>

      <button
        @click="pause"
        :disabled="!running"
        class="bg-yellow-600 hover:bg-yellow-700 text-white px-5 py-2 rounded"
      >Пауза</button>

      <button
        @click="resume"
        :disabled="running"
        class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded"
      >Продолжить</button>
    </div>

    <div class="mb-6 text-lg space-y-1">
      <p>Самокатов: {{ state?.scooters?.length || 0 }}</p>
      <p>Людей: {{ state?.people?.length || 0 }}</p>
      <p>Сломанных: {{ brokenScooters }}</p>
      <p>Завершённых поездок: {{ finishedTrips }}</p>
    </div>

    <MapCanvas :state="state" />
  </main>
</template>

<script setup>
import { ref, computed } from 'vue'
import MapCanvas from './components/MapCanvas.vue'

const state = ref(null)
const running = ref(false)
let ticker = null

async function loadState() {
  const res = await fetch('/api/state')
  state.value = await res.json()
}

async function start() {
  await fetch('/api/start?people=10&scooters_per_station=3', { method: 'POST' })
  running.value = true
  await loadState()
  ticker = setInterval(() => tick(), 100)  // тик каждые 100 мс для плавности
}

function pause() {
  running.value = false
  clearInterval(ticker)
}

function resume() {
  running.value = true
  ticker = setInterval(() => tick(), 100)
}

async function tick() {
  const res = await fetch('/api/tick')
  state.value = await res.json()
}

const brokenScooters = computed(() =>
  state.value?.scooters?.filter(s => s.is_broken).length || 0
)
const finishedTrips = computed(() =>
  state.value?.trips?.filter(t => t.finished).length || 0
)
</script>

<style scoped>
button {
  cursor: pointer;
  transition: background-color 0.2s ease;
}
</style>
