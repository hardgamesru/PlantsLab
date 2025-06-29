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
          <button @click="openPlantModal(gh.id)">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 6v3l4-4-4-4v3c-4.42 0-8 3.58-8 8 0 1.57.46 3.03 1.24 4.26L6.7 14.8c-.45-.83-.7-1.79-.7-2.8 0-3.31 2.69-6 6-6zm6.76 1.74L17.3 9.2c.44.84.7 1.79.7 2.8 0 3.31-2.69 6-6 6v-3l-4 4 4 4v-3c4.42 0 8-3.58 8-8 0-1.57-.46-3.03-1.24-4.26z"/>
            </svg>
            Посадить растение
          </button>
        </div>
      </div>

      <div v-else>
        <div class="info">
          <div class="header-row">
            <h3>Теплица {{ gh.id }}</h3>
            <button class="remove-btn" @click="$emit('remove-plant', gh.id)">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
              </svg>
            </button>
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
            <label :class="getValueColor(gh, 'temperature')">
              Температура: {{ gh.conditions.temperature }}°C
            </label>
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
            <label :class="getValueColor(gh, 'humidity')">
              Влажность: {{ gh.conditions.humidity }}%
            </label>
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
            <label :class="getValueColor(gh, 'light')">
              Свет: {{ gh.conditions.light }}%
            </label>
            <input
              type="range"
              min="0"
              max="100"
              step="1"
              v-model.number="gh.conditions.light"
              @change="updateGhConditions(gh.id)"
            >
          </div>

          <!-- Кнопка для установки оптимальных условий -->
          <button
            v-if="gh.plant"
            @click="setOptimalConditions(gh.id)"
            class="optimal-btn"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
            </svg>
            Оптимальные настройки
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно выбора растения -->
    <div class="modal-overlay" v-if="showPlantModal">
      <div class="plant-modal">
        <div class="modal-header">
          <h3>Выберите растение</h3>
          <button class="close-btn" @click="showPlantModal = false">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
              <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
            </svg>
          </button>
        </div>
        <div class="modal-content">
          <div class="plant-columns">
            <!-- Первый столбец -->
            <div class="plant-column">
              <button @click="selectPlant('gerbera')">
                <div class="plant-icon">🌼</div>
                <div>Гербера</div>
              </button>
              <button @click="selectPlant('larch')">
                <div class="plant-icon">🌲</div>
                <div>Лиственница</div>
              </button>
              <button @click="selectPlant('cactus')">
                <div class="plant-icon">🌵</div>
                <div>Кактус</div>
              </button>
              <button @click="selectPlant('orchid')">
                <div class="plant-icon">🌸</div>
                <div>Орхидея</div>
              </button>
            </div>

            <!-- Второй столбец -->
            <div class="plant-column">
              <button @click="selectPlant('sunflower')">
                <div class="plant-icon">🌻</div>
                <div>Подсолнух</div>
              </button>
              <button @click="selectPlant('flytrap')">
                <div class="plant-icon">🍃</div>
                <div>Венерина мухоловка</div>
              </button>
              <button @click="selectPlant('saguaro')">
                <div class="plant-icon">🌵</div>
                <div>Кактус Сагуаро</div>
              </button>
              <button @click="selectPlant('rafflesia')">
                <div class="plant-icon">🎪</div>
                <div>Раффлезия</div>
              </button>
            </div>
          </div>
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
      if (gh && gh.plant) {
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
      if (plant.health <= 0) return '#a0a0a0';
      if (plant.stage === 'Цветение') {
        switch(plant.name) {
          case 'Гербера': return '#FF69B4';
          case 'Орхидея': return '#DA70D6';
          case 'Подсолнух': return '#FFD700';
          case 'Венерина мухоловка': return '#FF5555';
          case 'Кактус Сагуаро': return '#FF69B4';
          case 'Раффлезия': return '#8B0000';
          default: return '#FF69B4';
        }
      }
      return plant.health > 70 ? '#4CAF50' : plant.health > 30 ? '#FFC107' : '#F44336';
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

    // Установка оптимальных условий
    const setOptimalConditions = (ghId) => {
      const gh = localGreenhouses.value.find(g => g.id === ghId);
      if (gh && gh.plant) {
        gh.conditions.temperature = gh.plant.optimal_temperature;
        gh.conditions.humidity = gh.plant.optimal_humidity;
        gh.conditions.light = gh.plant.optimal_light;
        updateGhConditions(ghId);
      }
    };

    // Определение цвета для значения параметра
    const getValueColor = (gh, conditionType) => {
      if (!gh.plant) return '';

      const currentValue = gh.conditions[conditionType];
      const optimalValue = gh.plant[`optimal_${conditionType}`];
      const threshold = gh.plant[`${conditionType}_threshold`];
      const diff = Math.abs(currentValue - optimalValue);

      if (diff <= threshold * 0.3) return 'value-optimal';
      if (diff <= threshold) return 'value-warning';
      return 'value-critical';
    };

    return {
      localGreenhouses,
      updateGhConditions,
      healthClass,
      plantStyle,
      getPlantColor,
      showPlantModal,
      openPlantModal,
      selectPlant,
      setOptimalConditions,
      getValueColor
    }
  }
}
</script>

<style scoped>
.map-row {
  display: flex;
  flex-wrap: nowrap;
  justify-content: center;
  gap: 20px;
  padding: 10px;
  overflow-x: auto;
}

.greenhouse {
  border-radius: 15px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.95);
  min-width: 250px;
  max-width: 300px;
  flex: 1;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.greenhouse:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2);
}

/* Стили для пустой теплицы */
.empty-greenhouse {
  background: rgba(255, 255, 255, 0.85);
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
  color: #2c3e50;
}

.plant-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 15px;
  width: 100%;
}

.plant-options button {
  padding: 12px 15px;
  background: linear-gradient(to right, #4a7bed, #3a6bdd);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.plant-options button:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
}

.plant-options button svg {
  width: 20px;
  height: 20px;
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
  cursor: pointer;
  color: #ff5555;
  padding: 5px;
  transition: all 0.3s ease;
}

.remove-btn:hover {
  color: #ff0000;
  transform: scale(1.1);
}

.remove-btn svg {
  width: 20px;
  height: 20px;
}

.plant-visualization {
  height: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 15px 0;
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
  background: linear-gradient(to right, #4a7bed, #3a6bdd);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.conditions-controls {
  margin-top: auto;
}

.control-group {
  margin-bottom: 15px;
}

.control-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #2c3e50;
}

.control-group input[type="range"] {
  width: 100%;
  height: 10px;
  -webkit-appearance: none;
  background: linear-gradient(to right, #4a7bed, #3a6bdd);
  border-radius: 5px;
  outline: none;
}

.control-group input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: white;
  border: 3px solid #4a7bed;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.health-good {
  color: #4CAF50;
  font-weight: bold;
}

.health-warning {
  color: #FF9800;
  font-weight: bold;
}

.health-critical {
  color: #F44336;
  font-weight: bold;
}

.health-dead {
  color: #9E9E9E;
  font-weight: bold;
  text-decoration: line-through;
}

.info {
  margin-bottom: 15px;
   color: #2c3e50;
}

.info h3 {
  color: #1e5799;
  margin-top: 0;
  font-size: 1.3em;
}

.info p {
  margin: 6px 0;
  font-size: 0.95em;

}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 20px;
  text-align: center;
  color: #2c3e50;
}

.value-optimal {
  color: #4CAF50;
  font-weight: bold;
}

.value-warning {
  color: #FF9800;
  font-weight: bold;
}

.value-critical {
  color: #F44336;
  font-weight: bold;
}

.optimal-btn {
  margin-top: 15px;
  padding: 12px 15px;
  background: linear-gradient(to right, #4CAF50, #3e8e41);
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  width: 100%;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.optimal-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25);
}

.optimal-btn svg {
  width: 20px;
  height: 20px;
}

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
  border-radius: 15px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
  width: 650px;
  max-width: 90%;
  overflow: hidden;
}

.modal-header {
  padding: 20px;
  background: linear-gradient(to right, #1e5799, #207cca);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.5em;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 2em;
  color: white;
  padding: 5px;
  transition: all 0.3s ease;
}

.close-btn:hover {
  transform: scale(1.1);
}

.close-btn svg {
  width: 24px;
  height: 24px;
}

.modal-content {
  padding: 25px;
}

.plant-columns {
  display: flex;
  gap: 25px;
  justify-content: center;
}

.plant-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 250px;
}

.plant-column button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 15px;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  color: #2c3e50;
  font-weight: 600;
  font-size: 1.1em;
}

.plant-column button:hover {
  background: rgba(74, 123, 237, 0.1);
  transform: translateY(-8px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  border-color: #4a7bed;
}

.plant-icon {
  font-size: 2.5em;
  margin-bottom: 12px;
  transition: transform 0.3s ease;
}

.plant-column button:hover .plant-icon {
  transform: scale(1.2);
}

.value-optimal {
  color: #4CAF50 !important; /* Зеленый - оптимально */
}

.value-warning {
  color: #FF9800 !important; /* Оранжевый - предупреждение */
}

.value-critical {
  color: #F44336 !important; /* Красный - критично */
}

</style>