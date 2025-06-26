<template>
  <div id="app">
    <h1>Лаборатория растений</h1>

    <!-- Инструкция и оптимальные значения -->
    <div class="instructions">
      <div class="optimal-values">
        <h2>Инструкция по выращиванию</h2>
        <div class="plant-instruction">
          <h3>Гербера</h3>
          <p>Оптимальная температура: 22±10°C</p>
          <p>Оптимальная влажность: 60±20%</p>
          <p>Оптимальное освещение: 70±30%</p>
          <p>Растение цветет при температуре ≥22°C</p>
        </div>
        <div class="plant-instruction">
          <h3>Лиственница</h3>
          <p>Оптимальная температура: 18±10°C</p>
          <p>Оптимальная влажность: 50±20%</p>
          <p>Оптимальное освещение: 60±30%</p>
          <p>Требуется стратификация (t < 5°C)</p>
        </div>
      </div>

      <div class="simulation-controls">
        <button @click="resetSystem">Перезапустить систему</button>
        <button @click="togglePause">{{ paused ? 'Пауза' : 'Старт' }}</button>
        <button @click="step">Шаг</button>
        <div class="time-control">
          <label>Скорость времени:</label>
          <input type="range" min="0.1" max="100" step="0.1" v-model="timeScale" @change="updateTimeScale">
          <span>{{ timeScale }}x</span>
        </div>
      </div>
    </div>

    <p class="virtual-time">Виртуальное время: {{ state.virtual_time.toFixed(1) }} у.е.</p>

    <!-- Два ряда теплиц -->
    <div class="greenhouse-rows">
      <div class="greenhouse-row">
        <Map :greenhouses="state.greenhouses.slice(0, 5)"
             @update-conditions="updateConditions"
             @set-plant="setPlant"
             @remove-plant="removePlant"/>
      </div>
      <div class="greenhouse-row">
        <Map :greenhouses="state.greenhouses.slice(5, 10)"
             @update-conditions="updateConditions"
             @set-plant="setPlant"
             @remove-plant="removePlant"/>
      </div>
    </div>
  </div>
</template>

<script>
import Map from './components/Map.vue'
import { ref, onMounted } from 'vue'

export default {
  components: { Map },
  setup() {
    const state = ref({ greenhouses: [], virtual_time: 0 })
    const paused = ref(true)
    const timeScale = ref(1.0)

     const setPlant = async (ghId, plantType) => {
      await fetch(`http://localhost:8000/api/greenhouse/${ghId}/plant/${plantType}`, {
        method: 'POST'
      })
      await fetchState()
    }

    const removePlant = async (ghId) => {
      await fetch(`http://localhost:8000/api/greenhouse/${ghId}/plant`, {
        method: 'DELETE'
      })
      await fetchState()
    }

    const fetchState = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/state')
        state.value = await response.json()
      } catch (error) {
        console.error('Ошибка получения данных:', error)
      }
    }

    const togglePause = async () => {
      await fetch('http://localhost:8000/api/pause', { method: 'POST' })
      paused.value = !paused.value
    }

    const step = async () => {
      await fetch('http://localhost:8000/api/step', { method: 'POST' })
      await fetchState()
    }

    const resetSystem = async () => {
      const response = await fetch('http://localhost:8000/api/reset', { method: 'POST' })
      const data = await response.json()
      // Синхронизируем состояние паузы
      paused.value = data.paused
      await fetchState()
    }

    const updateTimeScale = async () => {
      await fetch(`http://localhost:8000/api/time_scale/${timeScale.value}`, { method: 'POST' })
    }

    const updateConditions = async (ghId, newConditions) => {
      await fetch(`http://localhost:8000/api/greenhouse/${ghId}/conditions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newConditions)
      })
      await fetchState()
    }

    onMounted(() => {
      setInterval(fetchState, 1000)
    })

    return {
      state,
      paused,
      timeScale,
      togglePause,
      step,
      resetSystem,
      updateTimeScale,
      updateConditions,
      setPlant,
      removePlant
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
  padding: 0 20px;
}

.instructions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  flex-wrap: wrap;
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.optimal-values {
  text-align: left;
  flex: 2;
  min-width: 300px;
}

.plant-instruction {
  background-color: #e8f4f8;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.plant-instruction h3 {
  margin-top: 0;
  color: #2c3e50;
}

.simulation-controls {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  min-width: 250px;
}

.simulation-controls button {
  margin-bottom: 10px;
  padding: 8px 15px;
  width: 100%;
  max-width: 200px;
  background-color: #4a7bed;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.simulation-controls button:hover {
  background-color: #3a6bdd;
}

.time-control {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 200px;
  margin-top: 10px;
}

.time-control label {
  margin-right: 10px;
  font-size: 0.9em;
}

.time-control input {
  flex: 1;
}

.time-control span {
  margin-left: 10px;
  min-width: 40px;
}

.greenhouse-rows {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.greenhouse-row {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
}

.virtual-time {
  font-size: 1.2em;
  font-weight: bold;
  margin: 10px 0 20px;
  background-color: #e8f4f8;
  padding: 8px;
  border-radius: 4px;
}
</style>