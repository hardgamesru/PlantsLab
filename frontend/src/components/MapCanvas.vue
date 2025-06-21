<template>
  <!-- Контейнер для canvas-элемента -->
  <div>
    <!-- Сам холст: ref="canvas" позволяет получить к нему доступ в JS -->
    <canvas ref="canvas" width="1200" height="1200" class="border"> </canvas>
  </div>
</template>

<script setup>
// Импортируем реактивные хуки из Vue
import { ref, watch, onMounted } from 'vue'

// Определяем входные свойства компонента
// В props.state ожидается объект со свойствами: stations, scooters, people
const props = defineProps({
  state: Object
})

// Ссылка на DOM-элемент <canvas>
const canvas = ref(null)

// Наблюдатель: когда props.state изменится, вызываем функцию draw()
watch(
  () => props.state,
  () => {
    draw()
  }
)

// Хук mounted: когда компонент будет вставлен в DOM, сразу отрисуем
onMounted(() => {
  draw()
})

/**
 * Основная функция отрисовки на canvas
 */
function draw() {
  // Если ещё нет ссылки на canvas — выходим
  if (!canvas.value) return

  // Получаем 2D-контекст для рисования
  const ctx = canvas.value.getContext('2d')

  // Очищаем весь холст перед новой отрисовкой
  ctx.clearRect(0, 0, canvas.value.width, canvas.value.height)

  // Масштаб: переводим координаты из диапазона [0..100] в [0..800]
  // Здесь scale=8: 100 * 8 = 800
  const scale = 8

  // 1. Рисуем станции (синие квадраты)
  props.state?.stations?.forEach(st => {
    ctx.fillStyle = 'blue'                                       // Цвет заливки
    ctx.fillRect(
      st.x * scale - 7,                                          // X-координата с учётом масштаба и смещения
      st.y * scale - 7,                                          // Y-координата с учётом масштаба и смещения
      14,                                                        // Ширина квадрата
      14                                                         // Высота квадрата
    )
  })

  // 2. Рисуем самокаты (окружности)
  props.state?.scooters?.forEach(s => {
    ctx.beginPath()                                              // Начинаем новый путь
    ctx.arc(
      s.x * scale,                                              // X-координата центра
      s.y * scale,                                              // Y-координата центра
      7,                                                        // Радиус окружности
      0,                                                        // Угол начала (в радианах)
      2 * Math.PI                                              // Угол конца (полный круг)
    )
    // Цвет в зависимости от состояния самоката
    ctx.fillStyle = s.is_broken ? 'red' : 'green'
    ctx.fill()                                                   // Заливаем окружность
  })

  // 3. Рисуем людей (большее кольцо)
  props.state?.people?.forEach(p => {
    ctx.beginPath()
    ctx.arc(
      p.x * scale,
      p.y * scale,
      9,                                                        // Немного больше, чем самокат
      0,
      2 * Math.PI
    )
    // Цвет в зависимости, едет ли человек на самокате
    ctx.fillStyle = p.has_scooter ? 'purple' : 'gold'
    ctx.fill()
  })
}
</script>

<style scoped>
/* Стилевой scoped-блок: влияет только на этот компонент */
canvas {
  background-color: #f0f0f0;  /* светлый фон для контраста */
  border: 1px solid #ccc;     /* лёгкая рамка вокруг холста */
  display: block;             /* убрать строчно-блочный отступ */
  margin: 0 auto;             /* центрирование по горизонтали */
}
</style>
