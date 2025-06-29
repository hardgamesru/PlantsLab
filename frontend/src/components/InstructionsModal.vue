<template>
  <div class="modal-overlay" v-if="visible" @click.self="close">
    <div class="modal">
      <div class="modal-header">
        <h2>Инструкция по выращиванию растений</h2>
        <button class="close-btn" @click="close">✕</button>
      </div>

      <div class="modal-content">
        <div class="plant-instructions">
          <!-- Первый столбец -->
          <div class="column">
            <!-- Гербера -->
            <div class="plant-section">
              <div class="plant-header">
                <h3>Гербера</h3>
                <div class="plant-icon">🌹</div>
              </div>
              <div class="plant-image">
                <img src="@/assets/gerbera.png" alt="Гербера">
              </div>
              <ul>
                <li><strong>Оптимальная среда:</strong></li>
                <li>Температура: 22±10°C</li>
                <li>Влажность: 60±20%</li>
                <li>Освещение: 70±30%</li>
                <li><strong>Всходы:</strong> влажность >60%</li>
                <li><strong>Рост:</strong> около 80 у.е.)</li>
                <li><strong>Цветение:</strong> при ≥22°C каждые 20 у.е.</li>
                <li><strong>Особенности:</strong> Максимальный размер 5</li>
              </ul>
            </div>

            <!-- Лиственница -->
            <div class="plant-section">
              <div class="plant-header">
                <h3>Лиственница</h3>
                <div class="plant-icon">🌲</div>
              </div>
              <div class="plant-image">
                <img src="@/assets/larch.png" alt="Лиственница">
              </div>
              <ul>
                <li><strong>Оптимальная среда:</strong></li>
                <li>Температура: 18±30°C</li>
                <li>Влажность: 50±30%</li>
                <li>Освещение: 60±30%</li>
                <li><strong>Всходы:</strong> стратификация (<5°C в течение 5 у.е.)</li>
                <li><strong>Рост:</strong> около 4000 у.е.</li>
                <li><strong>Цветение:</strong> каждые 150 у.е. после созревания</li>
                <li><strong>Особенности:</strong> Требует холодной стратификации</li>
              </ul>
            </div>

            <!-- Кактус -->
            <div class="plant-section">
              <div class="plant-header">
                <h3>Кактус</h3>
                <div class="plant-icon">🌵</div>
              </div>
              <div class="plant-image">
                <img src="@/assets/cactus.png" alt="Кактус">
              </div>
              <ul>
                <li><strong>Оптимальная среда:</strong></li>
                <li>Температура: 30±10°C</li>
                <li>Влажность: 20±10%</li>
                <li>Освещение: 90±10%</li>
                <li><strong>Всходы:</strong> влажность <30%, свет > 70%</li>
                <li><strong>Рост:</strong> около 500 у.е.</li>
                <li><strong>Цветение:</strong> при ≥35°C каждые 40 у.е.</li>
                <li><strong>Особенности:</strong> Устойчив к засухе, медленный рост</li>
              </ul>
            </div>

            <!-- Орхидея -->
            <div class="plant-section">
              <div class="plant-header">
                <h3>Орхидея</h3>
                <div class="plant-icon">🌸</div>
              </div>
              <div class="plant-image">
                <img src="@/assets/orchid.png" alt="Орхидея">
              </div>
              <ul>
                <li><strong>Оптимальная среда:</strong></li>
                <li>Температура: 22±3°C</li>
                <li>Влажность: 80±10%</li>
                <li>Освещение: 40±20%</li>
                <li><strong>Всходы:</strong> влажность >70%, температура ± 22</li>
                <li><strong>Рост:</strong> около 100 у.е.</li>
                <li><strong>Цветение:</strong> при t=20-24°C и влажности >80%</li>
                <li><strong>Особенности:</strong> Чувствительна к перепадам</li>
              </ul>
            </div>
          </div>

          <!-- Второй столбец -->
          <div class="column">
            <!-- Подсолнух -->
            <div class="plant-section">
              <div class="plant-header">
                <h3>Подсолнух</h3>
                <div class="plant-icon">🌻</div>
              </div>
              <div class="plant-image">
                <img src="@/assets/sunflower.png" alt="Подсолнух">
              </div>
              <ul>
                <li><strong>Оптимальная среда:</strong></li>
                <li>Температура: 25±5°C</li>
                <li>Влажность: 50±10%</li>
                <li>Освещение: 95±5%</li>
                <li><strong>Всходы:</strong> свет >60%, влажность >40%</li>
                <li><strong>Рост:</strong> около 80 у.е.</li>
                <li><strong>Цветение:</strong> при свете >80% каждые 15 у.е.</li>
                <li><strong>Особенности:</strong> Быстро растет, требует много света</li>
              </ul>
            </div>

            <!-- Венерина мухоловка -->
            <div class="plant-section">
              <div class="plant-header">
                <h3>Венерина мухоловка</h3>
                <div class="plant-icon">🍃</div>
              </div>
              <div class="plant-image">
                <img src="@/assets/flytrap.png" alt="Венерина мухоловка">
              </div>
              <ul>
                <li><strong>Оптимальная среда:</strong></li>
                <li>Температура: 25±5°C</li>
                <li>Влажность: 80±10%</li>
                <li>Освещение: 50±20%</li>
                <li><strong>Всходы:</strong> влажность >85%, температура ±25</li>
                <li><strong>Рост:</strong> около 130 у.е.</li>
                <li><strong>Цветение:</strong> при стабильной t° (±2°C) каждые 30 у.е.</li>
                <li><strong>Особенности:</strong> Чувствительна к изменениям</li>
              </ul>
            </div>

            <!-- Кактус Сагуаро -->
            <div class="plant-section">
              <div class="plant-header">
                <h3>Кактус Сагуаро</h3>
                <div class="plant-icon">🌵</div>
              </div>
              <div class="plant-image">
                <img src="@/assets/saguaro.png" alt="Кактус Сагуаро">
              </div>
              <ul>
                <li><strong>Оптимальная среда:</strong></li>
                <li>Температура: 35±5°C</li>
                <li>Влажность: 15±5%</li>
                <li>Освещение: 95±5%</li>
                <li><strong>Всходы:</strong> влажность <20% + t>30°C</li>
                <li><strong>Рост:</strong> около 1100 у.е.</li>
                <li><strong>Цветение:</strong> при ≥40°C каждые 100 у.е.</li>
                <li><strong>Особенности:</strong> Экстремально медленный рост</li>
              </ul>
            </div>

            <!-- Раффлезия -->
            <div class="plant-section">
              <div class="plant-header">
                <h3>Раффлезия</h3>
                <div class="plant-icon">🎪</div>
              </div>
              <div class="plant-image">
                <img src="@/assets/rafflesia.png" alt="Раффлезия">
              </div>
              <ul>
                <li><strong>Оптимальная среда:</strong></li>
                <li>Температура: 28±2°C</li>
                <li>Влажность: 95±3%</li>
                <li>Освещение: 10±5%</li>
                <li><strong>Всходы:</strong> свет <5% + влажность >95%</li>
                <li><strong>Рост:</strong> 0.15/у.е. (до цветения: 30 у.е.)</li>
                <li><strong>Цветение:</strong> только в темноте (свет <5%)</li>
                <li><strong>Особенности:</strong> Живет 5-7 дней после цветения</li>
              </ul>
            </div>
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
  max-width: 1000px;
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

.modal-header button {
  background: none;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 15px;
  cursor: pointer;
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
.plant-instructions {
  display: flex;
  gap: 30px;
}

.column {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.plant-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  position: relative;
}

.plant-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.plant-icon {
  font-size: 2em;
}

.plant-image {
  height: 150px;
  border-radius: 6px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.plant-image img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}

.plant-section h3 {
  margin: 0;
  color: #2c3e50;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 10px;
}

.plant-section ul {
  padding-left: 0;
  list-style-type: none;
}

.plant-section li {
  margin-bottom: 12px;
  line-height: 1.5;
  padding-left: 20px;
  position: relative;
}

.plant-section li:before {
  content: "•";
  position: absolute;
  left: 0;
  color: #4CAF50;
  font-weight: bold;
}

.plant-section li strong {
  color: #2c3e50;
}
</style>