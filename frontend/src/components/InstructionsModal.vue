<template>
  <div class="modal-overlay" v-if="visible" @click.self="close">
    <div class="modal">
      <div class="modal-header">
        <h2>Инструкция по выращиванию растений</h2>
        <button class="close-btn" @click="close">✕</button>
      </div>

      <div class="modal-content">
        <div class="plant-instructions">

          <div class="plant-section">
            <h3>Гербера</h3>
            <ul>
              <li>Оптимальная температура: <strong>22±10°C</strong></li>
              <li>Оптимальная влажность: <strong>60±20%</strong></li>
              <li>Оптимальное освещение: <strong>70±30%</strong></li>
              <li>Цветение при ≥22°C каждые <strong>20 у.е.</strong></li>
              <li>Макс. размер: <strong>5</strong></li>
            </ul>
          </div>

          <div class="plant-section">
            <h3>Лиственница</h3>
            <ul>
              <li>Оптимальная температура: <strong>18±10°C</strong></li>
              <li>Оптимальная влажность: <strong>50±20%</strong></li>
              <li>Оптимальное освещение: <strong>60±30%</strong></li>
              <li>Требуется стратификация (<strong>&lt;5°C</strong>)</li>
              <li>Цветение каждые <strong>50 у.е.</strong></li>
            </ul>
          </div>


          <div class="plant-section">
            <h3>Кактус</h3>
            <ul>
              <li>Оптимальная температура: <strong>30±10°C</strong></li>
              <li>Оптимальная влажность: <strong>20±10%</strong></li>
              <li>Оптимальное освещение: <strong>90±10%</strong></li>
              <li>Цветение при ≥35°C каждые <strong>40 у.е.</strong></li>
              <li>Устойчив к засухе</li>
              <li>Макс. размер: <strong>3</strong></li>
            </ul>
          </div>

          <div class="plant-section">
            <h3>Орхидея</h3>
            <ul>
              <li>Оптимальная температура: <strong>22±3°C</strong></li>
              <li>Оптимальная влажность: <strong>80±10%</strong></li>
              <li>Оптимальное освещение: <strong>40±20%</strong></li>
              <li>Цветение при стабильной температуре каждые <strong>25 у.е.</strong></li>
              <li>Требует высокой влажности</li>
              <li>Макс. размер: <strong>4</strong></li>
            </ul>
          </div>

          <div class="plant-section">
            <h3>Подсолнух</h3>
            <ul>
              <li>Оптимальная температура: <strong>25±5°C</strong></li>
              <li>Оптимальная влажность: <strong>50±10%</strong></li>
              <li>Оптимальное освещение: <strong>95±5%</strong></li>
              <li>Цветение при >80% света каждые <strong>15 у.е.</strong></li>
              <li>Быстро растет</li>
              <li>Макс. размер: <strong>10</strong></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    visible: Boolean
  },
  emits: ['close'],
  setup(props, { emit }) {
    const close = () => {
      emit('close')
    }

    return {
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
  max-width: 600px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 20px;
  background-color: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5em;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.8em;
  cursor: pointer;
  color: white;
  padding: 5px;
  line-height: 1;
}

.modal-content {
  padding: 20px;
  overflow-y: auto;
}

.plant-instructions {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
}

.plant-section {
  flex: 1;
  min-width: 250px;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.plant-section h3 {
  margin-top: 0;
  color: #2c3e50;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 10px;
}

.plant-section ul {
  padding-left: 20px;
}

.plant-section li {
  margin-bottom: 10px;
  line-height: 1.5;
}
</style>