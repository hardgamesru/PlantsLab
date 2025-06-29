<template>
  <div class="modal-overlay" v-if="visible" @click.self="close">
    <div class="modal">
      <div class="modal-header">
        <h2>Журнал событий</h2>
        <div class="header-actions">
          <button @click="clearLog">Очистить журнал</button>
          <button class="close-btn" @click="close">✕</button>
        </div>
      </div>

      <div class="filter-section">
        <label>Теплица:</label>
        <select v-model="selectedGreenhouse">
          <option value="-1">Все теплицы</option>
          <option v-for="gh in greenhouses" :key="gh.id" :value="gh.id">
            Теплица {{ gh.id }}
          </option>
        </select>
      </div>

      <div class="log-container">
        <div v-if="logEntries.length === 0" class="empty-log">
          Журнал событий пуст
        </div>

        <div v-else class="log-entries">
          <div v-for="(entry, index) in logEntries" :key="index"
               :class="['log-entry', eventClass(entry)]">
            <div class="entry-header">
              <span class="real-time">{{ entry.real_time }}</span>
              <span class="event-type">Теплица {{ entry.greenhouse_id }}</span>
              <span class="event-type">{{ entry.event_type }}</span>
              <button class="delete-entry" @click="removeEntry(entry.id)">✕</button>
            </div>

            <div class="entry-content">
              <div class="greenhouse-info">
                <span class="event-type">Время: {{ entry.timestamp.toFixed(1) }} у.е.</span>
              </div>

              <div class="event-details">
                {{ entry.event_details }}
              </div>

              <div v-if="entry.plant_data" class="plant-data">
                <div class="plant-name">
                  <span>{{ entry.plant_data.name }}</span>
                  <span :class="['plant-stage', stageClass(entry.plant_data)]">
                    {{ entry.plant_data.stage }}
                  </span>
                </div>

                <div class="plant-stats">
                  <span>Размер: {{ entry.plant_data.size.toFixed(1) }}</span>
                  <span :class="healthClass(entry.plant_data)">
                    Здоровье: {{ entry.plant_data.health > 0 ?
                    entry.plant_data.health.toFixed(1) + '%' : 'мертво' }}
                  </span>
                  <span v-if="entry.plant_data.flowering_percent > 0">
                    Цветение: {{ entry.plant_data.flowering_percent.toFixed(1) }}%
                  </span>
                </div>
              </div>

              <div v-if="entry.conditions" class="conditions-data">
                <div class="condition">
                  <span class="condition-label">Температура:</span>
                  <span>{{ entry.conditions.temperature }}°C</span>
                </div>
                <div class="condition">
                  <span class="condition-label">Влажность:</span>
                  <span>{{ entry.conditions.humidity }}%</span>
                </div>
                <div class="condition">
                  <span class="condition-label">Освещение:</span>
                  <span>{{ entry.conditions.light }}%</span>
                </div>
              </div>
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
  props: {
    visible: Boolean,
    greenhouses: Array
  },
  emits: ['close'],
  setup(props, { emit }) {
    const selectedGreenhouse = ref(-1)
    const logEntries = ref([])

    const fetchLog = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/log?gh_id=${selectedGreenhouse.value}`)
        logEntries.value = await response.json()
      } catch (error) {
        console.error('Ошибка загрузки лога:', error)
      }
    }

    const clearLog = async () => {
      if (confirm('Вы уверены, что хотите очистить весь журнал?')) {
        await fetch('http://localhost:8000/api/log/clear', { method: 'POST' })
        await fetchLog()
      }
    }

    const removeEntry = async (entryId) => {
      if (confirm('Вы уверены, что хотите удалить эту запись?')) {
        await fetch(`http://localhost:8000/api/log/${entryId}`, { method: 'DELETE' })
        await fetchLog()
      }
    }

    const close = () => {
      emit('close')
    }

    const eventClass = (entry) => {
      const eventType = entry.event_type.toLowerCase()
      if (eventType.includes('посадка')) return 'event-plant-added'
      if (eventType.includes('удаление')) return 'event-plant-removed'
      if (eventType.includes('смерть')) return 'event-plant-died'
      if (eventType.includes('стадия')) return 'event-stage-changed'
      return ''
    }

    const healthClass = (plant) => {
      if (plant.health <= 0) return 'health-dead'
      if (plant.health > 70) return 'health-good'
      if (plant.health > 30) return 'health-warning'
      return 'health-critical'
    }

    const stageClass = (plant) => {
      const stage = plant.stage.toLowerCase()
      if (stage.includes('семя')) return 'stage-seed'
      if (stage.includes('росток')) return 'stage-sprout'
      if (stage.includes('рост')) return 'stage-growing'
      if (stage.includes('взрослое')) return 'stage-mature'
      if (stage.includes('цветение')) return 'stage-flowering'
      if (stage.includes('мертв')) return 'stage-dead'
      return ''
    }

    watch(selectedGreenhouse, fetchLog)
    watch(() => props.visible, (visible) => {
      if (visible) fetchLog()
    })

    return {
      selectedGreenhouse,
      logEntries,
      fetchLog,
      clearLog,
      removeEntry,
      close,
      eventClass,
      healthClass,
      stageClass
    }
  }
}
</script>

<style scoped>
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
  backdrop-filter: blur(2px);
}

.modal {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 900px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  color: #2c3e50;
}

.modal-header {
  padding: 20px;
  background: linear-gradient(to right, #1e5799, #207cca);
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5em;
}

.header-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.header-actions button {
  background: none;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  cursor: pointer;
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

.filter-section {
  padding: 15px 20px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #e0e0e0;
  color: black;
}

.filter-section label {
  margin-right: 10px;
  font-weight: 500;
  color: black;
}

.filter-section select {
  padding: 8px 12px;
  border-radius: 6px;
  border: 1px solid #ddd;
  background-color: white;
  font-size: 1em;
  width: 200px;
}

.log-container {
  overflow-y: auto;
  padding: 10px;
}

.empty-log {
  text-align: center;
  padding: 40px 20px;
  color: #777;
  font-style: italic;
}

.log-entries {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 10px;
}

.log-entry {
  border-radius: 8px;
  padding: 15px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 4px solid #ccc;
}

.log-entry:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

/* Цвета событий */
.event-plant-added {
  border-left-color: #4CAF50;
  background-color: #e8f5e9;
}

.event-plant-removed {
  border-left-color: #FF9800;
  background-color: #fff3e0;
}

.event-plant-died {
  border-left-color: #f44336;
  background-color: #ffebee;
}

.event-stage-changed {
  border-left-color: #2196F3;
  background-color: #e3f2fd;
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.real-time {
  font-weight: 600;
  color: #555;
}

.event-type {
  font-weight: bold;
  font-size: 1.1em;
  flex-grow: 1;
  text-align: center;
}

.delete-entry {
  background: none;
  border: none;
  color: #999;
  font-size: 1.2em;
  cursor: pointer;
  padding: 5px;
  transition: color 0.2s;
}

.delete-entry:hover {
  color: #f44336;
}

.entry-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.greenhouse-info {
  grid-column: span 2;
  display: flex;
  gap: 10px;
  font-size: 0.9em;
  color: #666;
  margin-bottom: 5px;
}

.gh-id {
  font-weight: 600;
}

.event-details {
  grid-column: span 2;
  font-weight: 500;
  margin-bottom: 10px;
  padding: 8px;
  background-color: rgba(255, 255, 255, 0.7);
  border-radius: 4px;
}

.plant-data, .conditions-data {
  padding: 10px;
  border-radius: 6px;
  background-color: white;
}

.plant-data {
  border: 1px solid #e0e0e0;
}

.conditions-data {
  border: 1px solid #bbdefb;
  background-color: #e3f2fd;
}

.plant-name {
  display: flex;
  justify-content: space-between;
  font-weight: 600;
  margin-bottom: 8px;
  padding-bottom: 5px;
  border-bottom: 1px dashed #eee;
}

.plant-stats {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 0.9em;
}

.condition {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
}

.condition-label {
  font-weight: 500;
  color: #555;
}

/* Цвета здоровья */
.health-good {
  color: #4CAF50;
  font-weight: 600;
}

.health-warning {
  color: #FF9800;
  font-weight: 600;
}

.health-critical {
  color: #f44336;
  font-weight: 600;
}

.health-dead {
  color: #757575;
  font-weight: 600;
}

/* Цвета стадий */
.stage-seed {
  color: #8d6e63;
  font-weight: 600;
}

.stage-sprout {
  color: #7cb342;
  font-weight: 600;
}

.stage-growing {
  color: #43a047;
  font-weight: 600;
}

.stage-mature {
  color: #2e7d32;
  font-weight: 600;
}

.stage-flowering {
  color: #ab47bc;
  font-weight: 600;
}

.stage-dead {
  color: #757575;
  font-weight: 600;
}

@media (max-width: 768px) {
  .entry-content {
    grid-template-columns: 1fr;
  }

  .plant-data, .conditions-data {
    grid-column: span 1;
  }
}
</style>