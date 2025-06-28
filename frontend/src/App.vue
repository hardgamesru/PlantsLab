<template>
  <div id="app">
    <h1>Лаборатория растений</h1>

    <div class="instructions">
      <div class="quick-guide">
        <h2>Краткое руководство</h2>
        <p>В этой программе вы можете управлять теплицами и выращивать растения.
           Для начала выберите теплицу и посадите растение (герберу или лиственницу).
           Управляйте условиями в теплице с помощью ползунков.
           Следите за здоровьем растения и его стадиями роста.
           Используйте кнопки управления временем для контроля над симуляцией.</p>
      </div>

      <div class="simulation-controls">
        <button @click="resetSystem">Перезапустить систему</button>
        <button @click="togglePause">{{ paused ? 'Старт' : 'Пауза' }}</button>
        <button @click="step">Шаг</button>
        <button @click="showInstructionsModal = true">Инструкция по выращиванию</button>
        <button @click="showLogModal = true">Показать лог</button>
      </div>
    </div>

    <LogModal
      :visible="showLogModal"
      :greenhouses="state.greenhouses"
      @close="showLogModal = false"
    />

    <InstructionsModal
      :visible="showInstructionsModal"
      @close="showInstructionsModal = false"
    />

    <div class="time-bar">
      <p class="virtual-time">Виртуальное время: {{ state.virtual_time.toFixed(1) }} у.е.</p>
      <span>{{ timeScale }}x</span>
      <div class="time-control-bar">
        <div class="time-buttons-left">
          <button @click="adjustTimeScale(-10)">-10</button>
          <button @click="adjustTimeScale(-1)">-1</button>
        </div>

        <input type="range" min="0.1" max="100" step="0.1" v-model.number="timeScale" @change="updateTimeScale">

        <div class="time-buttons-right">
          <button @click="adjustTimeScale(1)">+1</button>
          <button @click="adjustTimeScale(10)">+10</button>
        </div>
      </div>
      <div class="time-presets">
        <button @click="setTimeScale(1)">x1</button>
        <button @click="setTimeScale(10)">x10</button>
        <button @click="setTimeScale(100)">x100</button>
      </div>
    </div>

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
import LogModal from './components/LogModal.vue'
import InstructionsModal from './components/InstructionsModal.vue'
import { ref, onMounted } from 'vue'

export default {
  components: { Map, LogModal, InstructionsModal },
  setup() {
    const state = ref({ greenhouses: [], virtual_time: 0 })
    const paused = ref(true)
    const timeScale = ref(1.0)
    const showLogModal = ref(false)
    const showInstructionsModal = ref(false)

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
      paused.value = data.paused
      timeScale.value = data.time_scale
      await fetchState()
    }

    const updateTimeScale = async () => {
      await fetch(`http://localhost:8000/api/time_scale/${timeScale.value}`, { method: 'POST' })
    }

    const setTimeScale = async (value) => {
      timeScale.value = value
      await updateTimeScale()
    }

    const adjustTimeScale = async (delta) => {
      timeScale.value = Math.max(0.1, Math.min(100, parseFloat((timeScale.value + delta).toFixed(1))))
      await updateTimeScale()
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
      showLogModal,
      showInstructionsModal,
      togglePause,
      step,
      resetSystem,
      updateTimeScale,
      updateConditions,
      setPlant,
      removePlant,
      setTimeScale,
      adjustTimeScale
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

.quick-guide {
  text-align: left;
  flex: 2;
  min-width: 300px;
  font-size: 20px;
}

.quick-guide h2 {
  margin-top: 0;
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
  max-width: 250px;
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

.time-bar {
  background-color: #e8f4f8;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.virtual-time {
  font-size: 1.2em;
  font-weight: bold;
  margin: 0 0 10px;
}

.time-control-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  max-width: 600px;
}

.time-control-bar input[type="range"] {
  flex: 1;
}

.time-buttons-left, .time-buttons-right {
  display: flex;
  gap: 5px;
}

.time-buttons-left button,
.time-buttons-right button {
  padding: 5px 10px;
  font-size: 0.9em;
  background-color: #4a7bed;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.time-buttons-left button:hover,
.time-buttons-right button:hover {
  background-color: #3a6bdd;
}

.time-presets {
  margin-top: 10px;
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}

.time-presets button {
  padding: 5px 10px;
  font-size: 0.9em;
  background-color: #4a7bed;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.time-presets button:hover {
  background-color: #3a6bdd;
}

.time-presets span {
  font-weight: bold;
}

.time-control-extended label {
  margin-bottom: 5px;
}

.time-control-extended input {
  width: 100%;
  margin-bottom: 10px;
}

.time-control-extended span {
  margin-bottom: 10px;
  font-weight: bold;
}


.time-buttons button {
  padding: 5px 10px;
  font-size: 0.9em;
  background-color: #4a7bed;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.time-buttons button:hover {
  background-color: #3a6bdd;
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
</style>
