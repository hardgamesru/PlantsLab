<template>
  <div class="map-row">
    <div
      class="greenhouse"
      v-for="gh in greenhouses"
      :key="gh.id"
      :class="{ 'dead-plant': gh.plant.health <= 0 }"
    >
      <div class="info">
        <h3>Теплица {{ gh.id }}</h3>
        <p>{{ gh.plant.name }}</p>
        <p>Стадия: {{ gh.plant.stage }}</p>
        <p v-if="gh.plant.flowering_percent > 0">Цветение: {{ gh.plant.flowering_percent.toFixed(1) }}%</p>
        <p :class="{
          'health-good': gh.plant.health > 70,
          'health-warning': gh.plant.health > 30 && gh.plant.health <= 70,
          'health-critical': gh.plant.health > 0 && gh.plant.health <= 30,
          'health-dead': gh.plant.health <= 0
        }">
          Здоровье: {{ gh.plant.health > 0 ? gh.plant.health.toFixed(1) + '%' : 'мертво' }}
        </p>
      </div>

      <!-- Визуализация растения -->
      <div class="plant-visualization">
        <div
          class="plant"
          :style="{
            width: (gh.plant.size * 20) + 'px',
            height: (gh.plant.size * 20) + 'px',
            backgroundColor: getPlantColor(gh.plant),
            opacity: gh.plant.health > 0 ? 1 : 0.5
          }"
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
</template>

<script>
import { ref, watch } from 'vue'

export default {
  props: ['greenhouses'],
  emits: ['update-conditions'],
  setup(props, { emit }) {
    const localGreenhouses = ref(JSON.parse(JSON.stringify(props.greenhouses)))

    watch(() => props.greenhouses, (newVal) => {
      localGreenhouses.value = JSON.parse(JSON.stringify(newVal))
    }, { deep: true })

    const updateGhConditions = (ghId) => {
      const gh = localGreenhouses.value.find(g => g.id === ghId)
      if (gh) {
        emit('update-conditions', ghId, {
          temperature: gh.conditions.temperature,
          humidity: gh.conditions.humidity,
          light: gh.conditions.light
        })
      }
    }

    const getPlantColor = (plant) => {
      if (plant.health <= 0) return 'gray';
      if (plant.stage === 'Цветение') return 'pink';
      return plant.health > 70 ? 'green' : plant.health > 30 ? 'yellow' : 'red';
    }

    return {
      localGreenhouses,
      updateGhConditions,
      getPlantColor
    }
  }
}
</script>

<style>
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