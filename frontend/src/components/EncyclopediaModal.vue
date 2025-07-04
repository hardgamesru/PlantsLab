<template>
  <div class="modal-overlay" v-if="visible" @click.self="close">
    <div class="encyclopedia-modal">
      <div class="modal-header">
        <h2>Ботаническая энциклопедия растений</h2>
        <button class="close-btn" @click="close">✕</button>
      </div>

      <div class="modal-content">
        <div class="plant-entry">
          <h3>🌺 Гербера (Gerbera)</h3>
          <p><strong>Семейство:</strong> Астровые (Asteraceae)</p>
          <p><strong>Происхождение:</strong> Южная Африка, Азия, Южная Америка</p>
          <p><strong>Описание:</strong> Многолетнее травянистое растение с крупными яркими соцветиями-корзинками диаметром 4-15 см.
          Листья собраны в прикорневую розетку, длиной до 35 см. Цветы бывают всех цветов радуги, кроме синего.
          В природе насчитывается около 80 видов, в культуре - тысячи сортов.</p>
          <p><strong>Интересный факт:</strong> Гербера занимает 5-е место по популярности среди цветов в мире после роз, гвоздик, тюльпанов и хризантем.</p>
        </div>

        <div class="plant-entry">
          <h3>🌲 Лиственница (Larix)</h3>
          <p><strong>Семейство:</strong> Сосновые (Pinaceae)</p>
          <p><strong>Происхождение:</strong> Северное полушарие (Сибирь, Канада, Европа)</p>
          <p><strong>Описание:</strong> Хвойное дерево высотой до 50 м с пирамидальной кроной. Единственный род хвойных,
          сбрасывающий хвою на зиму. Шишки мелкие (1-4 см), созревают осенью. Древесина плотная, смолистая,
          устойчивая к гниению. Продолжительность жизни - 300-500 лет.</p>
          <p><strong>Интересный факт:</strong> Венеция построена на лиственничных сваях, которые за 1000 лет не только не сгнили, но и окаменели.</p>
        </div>

        <div class="plant-entry">
          <h3>🌵 Кактус (Cactaceae)</h3>
          <p><strong>Семейство:</strong> Кактусовые</p>
          <p><strong>Происхождение:</strong> Пустыни Северной и Южной Америки</p>
          <p><strong>Описание:</strong> Суккулентные растения с мясистыми стеблями, видоизмененными в колючки листьями
          и специальными тканями для накопления воды. Размеры варьируются от 1 см до 20 м в высоту.
          Цветы часто крупные, яркие, с множеством лепестков. Многие виды цветут только ночью.</p>
          <p><strong>Интересный факт:</strong> Самый большой кактус - карнегия гигантская (сагуаро) достигает высоты 15 м и веса 6-10 тонн.</p>
        </div>

        <div class="plant-entry">
          <h3>🌸 Орхидея (Orchidaceae)</h3>
          <p><strong>Семейство:</strong> Орхидные</p>
          <p><strong>Происхождение:</strong> Тропические леса по всему миру</p>
          <p><strong>Описание:</strong> Одно из самых крупных семейств цветковых растений - более 28 000 видов.
          Отличаются сложными цветками зигоморфного строения с уникальными механизмами опыления.
          Многие виды - эпифиты, растущие на деревьях. Некоторые виды полностью лишены хлорофилла
          и паразитируют на грибах.</p>
          <p><strong>Интересный факт:</strong> Семена орхидей - самые мелкие в мире, в 1 грамме может содержаться до 4 миллионов семян.</p>
        </div>

        <div class="plant-entry">
          <h3>🌻 Подсолнух (Helianthus annuus)</h3>
          <p><strong>Семейство:</strong> Астровые</p>
          <p><strong>Происхождение:</strong> Северная Америка</p>
          <p><strong>Описание:</strong> Однолетнее травянистое растение высотой 0,6-3 м с крупными соцветиями-корзинками
          диаметром 10-50 см. Обладает гелиотропизмом - поворачивается вслед за солнцем в течение дня.
          Плоды - семянки с высоким содержанием масла (до 50%). Основная масличная культура в России.</p>
          <p><strong>Интересный факт:</strong> Самый высокий подсолнух достиг 9,17 м (высота трехэтажного дома), выращен в Германии.</p>
        </div>

        <div class="plant-entry">
          <h3>🍃 Венерина мухоловка (Dionaea muscipula)</h3>
          <p><strong>Семейство:</strong> Росянковые</p>
          <p><strong>Происхождение:</strong> Болота Северной и Южной Каролины (США)</p>
          <p><strong>Описание:</strong> Небольшое хищное растение высотой 10-15 см. Листья образуют розетку вокруг цветоноса.
          Ловчий аппарат - видоизмененные листья с зубцами по краям и чувствительными волосками внутри.
          Захлопывается за 0,1 секунды при касании волосков. Переваривает насекомых за 5-12 дней.</p>
          <p><strong>Интересный факт:</strong> Может "считать" прикосновения - ловушка срабатывает только после двух касаний с интервалом до 20 секунд.</p>
        </div>

        <div class="plant-entry">
          <h3>🌵 Кактус Сагуаро (Carnegiea gigantea)</h3>
          <p><strong>Семейство:</strong> Кактусовые</p>
          <p><strong>Происхождение:</strong> Пустыня Сонора (США, Мексика)</p>
          <p><strong>Описание:</strong> Гигантский древовидный кактус высотой до 15-18 м, массой 6-10 тонн.
          Растет очень медленно - первые боковые ветви появляются в 50-70 лет. Цветет в мае-июне белыми восковыми
          цветами, которые раскрываются ночью. Плоды - красные ягоды, съедобные и питательные.</p>
          <p><strong>Интересный факт:</strong> Является символом штата Аризона и охраняется законом - за повреждение кактуса грозит до 25 лет тюрьмы.</p>
        </div>

        <div class="plant-entry">
          <h3>🎪 Раффлезия (Rafflesia)</h3>
          <p><strong>Семейство:</strong> Раффлезиевые</p>
          <p><strong>Происхождение:</strong> Тропические леса Юго-Восточной Азии</p>
          <p><strong>Описание:</strong> Паразитическое растение без листьев, стеблей и корней. Развивается внутри
          лиан рода Tetrastigma. Цветки - самые крупные в мире, достигают 1 м в диаметре и веса 10 кг.
          Издают сильный запах гниющего мяса для привлечения мух-опылителей. Вегетационный цикл - 3-4 года.</p>
          <p><strong>Интересный факт:</strong> Rafflesia arnoldii имеет самый большой цветок на планете - до 106 см в диаметре.</p>
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
}

.encyclopedia-modal {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 900px;
  height: 90vh; /* Увеличена высота до 90% экрана */
  display: flex;
  flex-direction: column;
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

.modal-header h2 {
  margin: 0;
  font-size: 1.8em;
  font-weight: 600;
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
  overflow-y: auto;
  background: linear-gradient(to bottom, #f8fdff, #e6f4f9);
  height: 100%;
}

.plant-entry {
  margin-bottom: 35px;
  padding-bottom: 30px;
  border-bottom: 2px dashed #c1e0f0;
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.plant-entry:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 20px;
}

.plant-entry h3 {
  color: #2c5a7a;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.5em;
  border-left: 5px solid #207cca;
  padding-left: 15px;
}

.plant-entry p {
  line-height: 1.7;
  color: #333;
  margin-bottom: 12px;
  font-size: 1.05em;
}

.plant-entry strong {
  color: #2c5a7a;
}

/* Стили для скроллбара */
.modal-content::-webkit-scrollbar {
  width: 10px;
}

.modal-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.modal-content::-webkit-scrollbar-thumb {
  background: #207cca;
  border-radius: 10px;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background: #3e8e41;
}
</style>