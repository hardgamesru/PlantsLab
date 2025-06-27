<template>
  <div class="map-row">
    <div
      class="greenhouse"
      v-for="gh in greenhouses"
      :key="gh.id"
      :class="{ 'empty-greenhouse': !gh.plant }"
    >
      <div v-if="!gh.plant" class="empty-state">
        <h3>Теплица {{ gh.id }}</h3>
        <p>Растение не посажено</p>
        <div class="plant-options">
          <button @click="openPlantModal(gh.id)">Посадить растение</button>
        </div>
      </div>

      <div v-else>
        <div class="info">
          <div class="header-row">
            <h3>Теплица {{ gh.id }}</h3>
            <button class="remove-btn" @click="$emit('remove-plant', gh.id)">✕</button>
          </div>
          <p>{{ gh.plant.name }}</p>
          <p>Стадия: {{ gh.plant.stage }}</p>
          <p v-if="gh.plant.flowering_percent > 0">Цветение: {{ gh.plant.flowering_percent.toFixed(1) }}%</p>
          <p :class="healthClass(gh.plant)">
            Здоровье: {{ gh.plant.health > 0 ? gh.plant.health.toFixed(1) + '%' : 'мертво' }}
          </p>
        </div>

        <!-- Визуализация растения -->
        <div class="plant-visualization">
          <div
            class="plant"
            :style="plantStyle(gh.plant)"
          ></div>

          <!-- Индикатор цветения -->
          <div v-if="gh.plant.flowering_percent > 0" class="flower-indicator">
            <div class="flower-progress" :style="{ width: gh.plant.flowering_percent + '%' }"></div>
          </div>
        </div>

        <!-- Управление условиями -->
        <div class="conditions-controls">
          <div class="control-group">
            <label>Температура: {{ gh.conditions.temperature }}°C</label>
            <input
              type="range"
              min="0"
              max="50"
              step="1"
              v-model.number="gh.conditions.temperature"
              @change="updateGhConditions(gh.id)"
            >
          </div>

          <div class="control-group">
            <label>Влажность: {{ gh.conditions.humidity }}%</label>
            <input
              type="range"
              min="0"
              max="100"
              step="1"
              v-model.number="gh.conditions.humidity"
              @change="updateGhConditions(gh.id)"
            >
          </div>

          <div class="control-group">
            <label>Свет: {{ gh.conditions.light }}%</label>
            <input
              type="range"
              min="0"
              max="100"
              step="1"
              v-model.number="gh.conditions.light"
              @change="updateGhConditions(gh.id)"
            >
          </div>
        </div>
      </div>
    </div>
    <div class="modal-overlay" v-if="showPlantModal">
      <div class="plant-modal">
        <div class="modal-header">
          <h3>Выберите растение</h3>
          <button class="close-btn" @click="showPlantModal = false">✕</button>
        </div>
        <div class="modal-content">
          <button @click="selectPlant('gerbera')">Гербера</button>
          <button @click="selectPlant('larch')">Лиственница</button>
          <button @click="selectPlant('cactus')">Кактус</button>
          <button @click="selectPlant('orchid')">Орхидея</button>
          <button @click="selectPlant('sunflower')">Подсолнух</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'

export default {
  props: ['greenhouses'],
  emits: ['update-conditions', 'set-plant', 'remove-plant'],
  setup(props, { emit }) {
    const localGreenhouses = ref(JSON.parse(JSON.stringify(props.greenhouses)))

    watch(() => props.greenhouses, (newVal) => {
      localGreenhouses.value = JSON.parse(JSON.stringify(newVal))
    }, { deep: true })

    const updateGhConditions = (ghId) => {
      const gh = localGreenhouses.value.find(g => g.id === ghId)
      if (gh && gh.plant) {  // Только если есть растение
        emit('update-conditions', ghId, {
          temperature: gh.conditions.temperature,
          humidity: gh.conditions.humidity,
          light: gh.conditions.light
        })
      }
    }

    const healthClass = (plant) => {
      if (plant.health <= 0) return 'health-dead';
      if (plant.health > 70) return 'health-good';
      if (plant.health > 30) return 'health-warning';
      return 'health-critical';
    }

    const plantStyle = (plant) => {
      const size = plant.size * 20;
      return {
        width: `${size}px`,
        height: `${size}px`,
        backgroundColor: getPlantColor(plant),
        opacity: plant.health > 0 ? 1 : 0.5
      };
    }

    const getPlantColor = (plant) => {
      if (plant.health <= 0) return 'gray';
      if (plant.stage === 'Цветение') {
        // Разные цвета цветения для разных растений
        if (plant.name === 'Кактус') return '#FF69B4'; // Розовый
        if (plant.name === 'Орхидея') return '#DA70D6'; // Орхидейный
        if (plant.name === 'Подсолнух') return '#FFD700'; // Золотой
        return 'pink'; // По умолчанию
      }
      return plant.health > 70 ? 'green' : plant.health > 30 ? 'yellow' : 'red';
    }

    const showPlantModal = ref(false)
    const selectedGhId = ref(null)

    const openPlantModal = (ghId) => {
      selectedGhId.value = ghId
      showPlantModal.value = true
    }

    const selectPlant = (plantType) => {
      if (selectedGhId.value !== null) {
        emit('set-plant', selectedGhId.value, plantType)
      }
      showPlantModal.value = false
    }
    return {
      localGreenhouses,
      updateGhConditions,
      healthClass,
      plantStyle,
      getPlantColor,
      showPlantModal,
      openPlantModal,
      selectPlant
    }
  }
}
</script>

<style>
/* Стили для пустой теплицы */
.empty-greenhouse {
  background-color: #f0f8ff;
  border: 2px dashed #a0c5e8;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 20px;
  text-align: center;
}

.plant-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 15px;
  width: 100%;
}

.plant-options button {
  padding: 8px 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.plant-options button:hover {
  background-color: #3e8e41;
}

/* Стили для кнопки удаления */
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.remove-btn {
  background: none;
  border: none;
  font-size: 1.2em;
  cursor: pointer;
  color: #ff5555;
  padding: 5px;
}

.remove-btn:hover {
  color: #ff0000;
}
.map-row {
  display: flex;
  flex-wrap: nowrap;
  justify-content: center;
  gap: 20px;
  padding: 10px;
  overflow-x: auto;
}

.greenhouse {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
  min-width: 250px;
  max-width: 300px;
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
}

.greenhouse:hover {
  transform: scale(1.03);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.dead-plant {
  background-color: #ffeaea;
  border-color: #ffcccc;
}

.plant-visualization {
  height: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 10px 0;
}

.plant {
  border-radius: 50%;
  transition: all 0.5s ease;
  margin-bottom: 10px;
}

.flower-indicator {
  height: 8px;
  width: 100%;
  background-color: #e0e0e0;
  border-radius: 4px;
}

.flower-progress {
  height: 100%;
  background-color: #ff69b4;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.conditions-controls {
  margin-top: auto;
}

.control-group {
  margin-bottom: 10px;
}

.control-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 0.9em;
}

.control-group input[type="range"] {
  width: 100%;
}

.health-good {
  color: green;
  font-weight: bold;
}

.health-warning {
  color: orange;
}

.health-critical {
  color: red;
  font-weight: bold;
}

.health-dead {
  color: gray;
  text-decoration: line-through;
}

.info {
  margin-bottom: 10px;
}

.info p {
  margin: 3px 0;
  font-size: 0.9em;
}

/* Адаптивные стили */
@media (max-width: 1600px) {
  .greenhouse {
    min-width: 220px;
  }
}

@media (max-width: 1400px) {
  .greenhouse {
    min-width: 200px;
  }
}

@media (max-width: 1200px) {
  .greenhouse {
    min-width: 180px;
    padding: 10px;
  }
}

@media (max-width: 1000px) {
  .greenhouse {
    min-width: 160px;
  }
}
</style>

<style scoped>
/* Добавляем стили для модального окна */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.plant-modal {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 300px;
  overflow: hidden;
}

.modal-header {
  padding: 15px;
  background-color: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: white;
  padding: 5px;
}

.modal-content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.modal-content button {
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1em;
  transition: background-color 0.3s;
}

.modal-content button:hover {
  background-color: #3e8e41;
}
</style>