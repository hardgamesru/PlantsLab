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
            Выставить оптимальные настройки
          </button>
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
      if (plant.health <= 0) return 'gray';
      if (plant.stage === 'Цветение') {
        switch(plant.name) {
          case 'Гербера': return '#FF69B4';
          case 'Орхидея': return '#DA70D6';
          case 'Подсолнух': return '#FFD700';
          case 'Венерина мухоловка': return '#FF0000';
          case 'Кактус Сагуаро': return '#FF69B4';
          case 'Раффлезия': return '#8B0000';
          default: return 'pink';
        }
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
.header-row button {
  background: none;
  color: red;
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.header-row button:hover {
  background-color: #3a6bdd;
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

/* Стили для цветов значений параметров */
.value-optimal {
  color: #4CAF50; /* Зеленый */
  font-weight: bold;
}

.value-warning {
  color: #FF9800; /* Оранжевый */
}

.value-critical {
  color: #f44336; /* Красный */
  font-weight: bold;
}

/* Стили для кнопки оптимальных настроек */
.optimal-btn {
  margin-top: 10px;
  padding: 8px 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s;
}

.optimal-btn:hover {
  background-color: #3e8e41;
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
  width: 600px;
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
.modal-header button {
  background: none;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.modal-header button:hover {
  background-color: #3a6bdd;
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

.plant-columns {
  display: flex;
  gap: 20px;
}

.plant-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.plant-column button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 15px 10px;
  background-color: #4CAF50;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.plant-column button:hover {
  background-color: #e9f5e9;
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.plant-icon {
  font-size: 2em;
  margin-bottom: 8px;
}
</style>