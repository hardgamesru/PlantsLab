<template>
  <div class="modal-overlay" v-if="visible" @click.self="close">
    <div class="modal">
      <div class="modal-header">
        <h2>Журнал событий</h2>
        <button class="close-btn" @click="close">✕</button>
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
        <table class="log-table">
          <thead>
            <tr>
              <th>Время</th>
              <th>Теплица</th>
              <th>Темп.</th>
              <th>Влажн.</th>
              <th>Свет</th>
              <th>Растение</th>
              <th>Стадия</th>
              <th>Размер</th>
              <th>Здоровье</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in logEntries" :key="entry.timestamp">
              <td>{{ entry.timestamp.toFixed(1) }}</td>
              <td>{{ entry.greenhouse_id }}</td>
              <td>{{ entry.conditions.temperature }}°C</td>
              <td>{{ entry.conditions.humidity }}%</td>
              <td>{{ entry.conditions.light }}%</td>
              <td>{{ entry.plant_data?.name || '-' }}</td>
              <td>{{ entry.plant_data?.stage || '-' }}</td>
              <td>{{ entry.plant_data?.size?.toFixed(1) || '-' }}</td>
              <td>{{ entry.plant_data?.health?.toFixed(1) || '-' }}%</td>
            </tr>
          </tbody>
        </table>
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

    const close = () => {
      emit('close')
    }

    watch(selectedGreenhouse, fetchLog)
    watch(() => props.visible, (visible) => {
      if (visible) fetchLog()
    })

    return {
      selectedGreenhouse,
      logEntries,
      close
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
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 200; /* Должен быть выше z-index кнопки */
}

.modal {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 1200px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  position: relative; /* Важно для позиционирования */
  z-index: 201; /* Выше чем оверлей */
}
.modal-header {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5em;
  cursor: pointer;
  color: #666;
}

.filter-section {
  padding: 15px 20px;
  border-bottom: 1px solid #eee;
}

.filter-section label {
  margin-right: 10px;
}

.filter-section select {
  padding: 5px 10px;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.log-container {
  overflow-y: auto;
  padding: 0 10px;
}

.log-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9em;
}

.log-table th, .log-table td {
  padding: 8px 10px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.log-table th {
  background-color: #f5f7fa;
  position: sticky;
  top: 0;
}

.log-table tr:hover {
  background-color: #f9f9f9;
}
</style>