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
        <button @click="resetSystem">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 5V1L7 6l5 5V7c3.31 0 6 2.69 6 6s-2.69 6-6 6-6-2.69-6-6H4c0 4.42 3.58 8 8 8s8-3.58 8-8-3.58-8-8-8z"/>
          </svg>
          Перезапустить
        </button>
        <button @click="togglePause">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path v-if="paused" d="M8 5v14l11-7z"/>
            <path v-else d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
          </svg>
          {{ paused ? 'Старт' : 'Пауза' }}
        </button>
        <button @click="step">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M5 4v16h16V4H5zm2 2h12v12H7V6zm3 4v4h2v-4h-2zm4 0v4h2v-4h-2z"/>
          </svg>
          Шаг
        </button>
        <button @click="showInstructionsModal = true">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M11 7h2v2h-2zm0 4h2v6h-2zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
          </svg>
          Инструкция
        </button>
        <button @click="showLogModal = true">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H5.17l-.59.59-.58.58V4h16v12zM6 12h12v2H6zm0-3h12v2H6zm0-3h12v2H6z"/>
          </svg>
          Показать лог
        </button>
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
    <div class="encyclopedia-section">
      <div class="encyclopedia-content">
        <h2>Ботаническая энциклопедия растений</h2>
        <p>Узнайте интересные факты о растениях, которые вы выращиваете в теплицах.
        Наша энциклопедия содержит подробную информацию о происхождении, особенностях
        и уникальных свойствах каждого растения.</p>
        <button @click="showEncyclopediaModal = true">
          <span>Открыть энциклопедию</span>
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path d="M5 13h11.17l-4.88 4.88c-.39.39-.39 1.03 0 1.42.39.39 1.02.39 1.41 0l6.59-6.59a.996.996 0 0 0 0-1.41l-6.58-6.6a.996.996 0 1 0-1.41 1.41L16.17 11H5c-.55 0-1 .45-1 1s.45 1 1 1z"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Модальное окно энциклопедии -->
    <EncyclopediaModal
      :visible="showEncyclopediaModal"
      @close="showEncyclopediaModal = false"
    />
  </div>
</template>

<script>
import Map from './components/Map.vue'
import LogModal from './components/LogModal.vue'
import InstructionsModal from './components/InstructionsModal.vue'
import EncyclopediaModal from './components/EncyclopediaModal.vue'
import { ref, onMounted } from 'vue'

export default {
  components: { Map, LogModal, InstructionsModal, EncyclopediaModal },
  setup() {
    const state = ref({ greenhouses: [], virtual_time: 0 })
    const paused = ref(true)
    const timeScale = ref(1.0)
    const showLogModal = ref(false)
    const showInstructionsModal = ref(false)
    const showEncyclopediaModal = ref(false)

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
      adjustTimeScale,
      showEncyclopediaModal
    }
  }
}
</script>

<style>
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  text-align: center;
  color: white;
  padding: 20px;
  background: linear-gradient(135deg, #1e5799 0%, #207cca 51%, #2989d8 100%);
  min-height: 100vh;
  background-attachment: fixed;
}

h1 {
  font-size: 2.8rem;
  margin: 0 0 25px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  color: #fff;
  background: rgba(255, 255, 255, 0.1);
  padding: 15px;
  border-radius: 15px;
  display: inline-block;
}

.instructions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  flex-wrap: wrap;
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.quick-guide {
  text-align: left;
  flex: 2;
  min-width: 300px;
  font-size: 18px;
  color: #2c3e50;
}

.quick-guide h2 {
  margin-top: 0;
  color: #1e5799;
  font-size: 1.8rem;
  border-bottom: 2px solid #4a7bed;
  padding-bottom: 8px;
  margin-bottom: 15px;
}

.simulation-controls {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  min-width: 250px;
}

.simulation-controls button {
  margin-bottom: 12px;
  padding: 12px 20px;
  width: 100%;
  max-width: 250px;
  background: linear-gradient(to right, #4a7bed, #3a6bdd);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.simulation-controls button:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  background: linear-gradient(to right, #3a6bdd, #2a5bcd);
}

.simulation-controls button svg {
  width: 20px;
  height: 20px;
}

.time-bar {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 15px;
  margin-bottom: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  color: #2c3e50;
}

.virtual-time {
  font-size: 1.3em;
  font-weight: bold;
  margin: 0 0 15px;
  color: #1e5799;
}

.time-control-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  max-width: 600px;
  margin-bottom: 15px;
}

.time-control-bar input[type="range"] {
  flex: 1;
  height: 10px;
  -webkit-appearance: none;
  background: linear-gradient(to right, #4a7bed, #3a6bdd);
  border-radius: 5px;
  outline: none;
}

.time-control-bar input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: white;
  border: 3px solid #4a7bed;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.time-buttons-left, .time-buttons-right {
  display: flex;
  gap: 5px;
}

.time-buttons-left button,
.time-buttons-right button {
  padding: 8px 15px;
  font-size: 1em;
  background: linear-gradient(to right, #4a7bed, #3a6bdd);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.time-buttons-left button:hover,
.time-buttons-right button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
}

.time-presets {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
  justify-content: center;
}

.time-presets button {
  padding: 8px 20px;
  font-size: 1em;
  background: rgba(255, 255, 255, 0.9);
  color: #1e5799;
  border: 2px solid #4a7bed;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
}

.time-presets button:hover {
  background: #4a7bed;
  color: white;
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.greenhouse-rows {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.greenhouse-row {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.encyclopedia-section {
  margin: 40px auto;
  padding: 0;
  background: linear-gradient(135deg, rgba(30, 87, 153, 0.9) 0%, rgba(32, 124, 202, 0.9) 51%, rgba(41, 137, 216, 0.9) 100%);
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  overflow: hidden;
}

.encyclopedia-content {
  padding: 40px 30px;
  text-align: center;
  color: white;
}

.encyclopedia-content h2 {
  font-size: 2.2rem;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.encyclopedia-content p {
  font-size: 1.2rem;
  max-width: 800px;
  margin: 0 auto 30px;
  line-height: 1.7;
  opacity: 0.9;
}

.encyclopedia-content button {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 35px;
  background-color: white;
  color: #1e5799;
  border: none;
  border-radius: 50px;
  font-size: 1.3rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.encyclopedia-content button:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  background-color: #f8f9fa;
}

.encyclopedia-content button svg {
  width: 24px;
  height: 24px;
  transition: transform 0.3s ease;
}

.encyclopedia-content button:hover svg {
  transform: translateX(5px);
}

</style>