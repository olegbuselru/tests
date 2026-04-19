export const CLASSES = {
  blade: { id: 'blade', name: 'Клинок Рассвета', hp: 130, mana: 40, skill: 'arcSlash', desc: 'Надежный мечник с блоком и усиленной ближней атакой.' },
  arcanist: { id: 'arcanist', name: 'Эфирный Арканист', hp: 90, mana: 120, skill: 'riftBolt', desc: 'Дальнобойная магия, контроль и высокий burst.' },
  ranger: { id: 'ranger', name: 'Теневой Следопыт', hp: 105, mana: 75, skill: 'pierceShot', desc: 'Мобильный боец, уклонения и криты.' }
};

export const ITEMS = {
  herb: { id: 'herb', name: 'Лунная трава', type: 'consumable', hp: 25, desc: 'Пахнет дождем и холодной сталью.' },
  coreShard: { id: 'coreShard', name: 'Осколок Сердца Руин', type: 'quest', desc: 'Пульсирует, словно помнит тебя.' },
  ironCharm: { id: 'ironCharm', name: 'Железный оберег Милы', type: 'trinket', desc: 'Дарит +5 к максимальному HP.' }
};

export const ABILITIES = {
  arcSlash: { name: 'Дуговой разрез', dmg: 28, mana: 8, cooldown: 4 },
  riftBolt: { name: 'Разломный болт', dmg: 34, mana: 14, cooldown: 5 },
  pierceShot: { name: 'Пробивной выстрел', dmg: 24, mana: 10, cooldown: 3 }
};

export const NPCS = {
  nera: { id: 'nera', name: 'Нера Пепельная', tone: 'ироничная, теплая', hidden: 'ищет способ закрыть разломы и боится цены' },
  elder: { id: 'elder', name: 'Староста Орвейн', tone: 'прагматичный', hidden: 'скрывает факт сделки с руинами' },
  mila: { id: 'mila', name: 'Мила Травница', tone: 'добрая, нервная', hidden: 'ее брат пропал в башне' }
};

export const ENEMIES = {
  mossling: { id: 'mossling', name: 'Мшистый клык', hp: 40, atk: 8, xp: 25, speed: 80 },
  hollowScout: { id: 'hollowScout', name: 'Пустотный разведчик', hp: 58, atk: 11, xp: 35, speed: 95 },
  ruinWarden: { id: 'ruinWarden', name: 'Страж Реликтовой Башни', hp: 190, atk: 16, xp: 140, speed: 65, boss: true }
};

export const QUESTS = {
  q1_main: {
    id: 'q1_main', chapter: 1, title: 'Голос в корнях',
    description: 'Выжить, понять правила нового мира и найти проводника.',
    objectives: ['Выбрать класс', 'Поговорить с Нерой', 'Победить 2 мшистых клыка', 'Принять моральное решение у алтаря'],
    rewards: { xp: 120, items: ['herb'] }
  },
  q2_main: {
    id: 'q2_main', chapter: 2, title: 'Сердце Руин',
    description: 'Добраться до башни и добыть осколок до наступления тумана.',
    objectives: ['Поговорить со старостой', 'Исследовать руины', 'Победить Стража', 'Вернуть осколок в деревню'],
    rewards: { xp: 220, items: ['coreShard'] }
  },
  q2_side_herbs: {
    id: 'q2_side_herbs', chapter: 2, title: 'Тихие листья',
    description: 'Собрать 3 лунные травы для Милы.',
    objectives: ['Собрано трав: 0/3'], rewards: { xp: 80, items: ['ironCharm'] }
  },
  q2_side_scout: {
    id: 'q2_side_scout', chapter: 2, title: 'Следы в тумане',
    description: 'Уничтожить разведчика пустоты возле мельницы.',
    objectives: ['Победить 1 пустотного разведчика'], rewards: { xp: 90, items: ['herb'] }
  }
};

export const DIALOGUES = {
  introEcho: {
    start: { speaker: 'Эхо Мира', text: 'Ты умер в шуме металла и стекла. Но это не конец. Это... договор.', choices: [
      { text: 'Кто ты?', next: 'who' },
      { text: 'Я не просил этого.', next: 'deny' }
    ]},
    who: { speaker: 'Эхо Мира', text: 'Я память мира. Я шепот между слоями реальности. Встань — и выбери путь.', next: null },
    deny: { speaker: 'Эхо Мира', text: 'Никто не просит бурю. Но ты уже внутри нее.', next: null }
  },
  neraFirst: {
    start: { speaker: 'Нера', text: 'Судя по глазам, ты либо мертвец, либо новичок. Что предпочтительнее?', choices: [
      { text: 'Сарказм: а есть пакет “оба сразу”?', effect: { rel: ['nera', 1] }, next: 'sar' },
      { text: 'Доброта: мне нужна помощь.', effect: { rel: ['nera', 2] }, next: 'kind' },
      { text: 'Подозрительность: ты кто вообще?', effect: { rel: ['nera', -1] }, next: 'sus' }
    ]},
    sar: { speaker: 'Нера', text: 'Ха. Тогда живи достаточно долго, чтобы шутка не стала эпитафией.', next: null },
    kind: { speaker: 'Нера', text: 'Честный ответ. Редкость. Ладно, объясню основы и прикрою спину.', next: null },
    sus: { speaker: 'Нера', text: 'Та, кто может уйти. Но если хочешь выжить — держись рядом.', next: null }
  },
  altarChoice: {
    start: { speaker: 'Эхо Мира', text: 'У алтаря лежит раненный зверь и ржавый ключ. Спасти жизнь или взять инструмент силы?', choices: [
      { text: 'Спасти зверя', setFlag: ['altarMercy', true], next: 'mercy' },
      { text: 'Забрать ключ', setFlag: ['altarMercy', false], next: 'power' }
    ]},
    mercy: { speaker: 'Эхо Мира', text: 'Милосердие — долгий путь, но он оставляет свет.', next: null },
    power: { speaker: 'Эхо Мира', text: 'Сила открывает двери. Иногда — клетки.', next: null }
  }
};

export const CHAPTERS = {
  1: { id: 1, name: 'Глава I: Пробуждение в ином мире', next: 2 },
  2: { id: 2, name: 'Глава II: Край леса и Реликтовая башня', next: null }
};

// Extension examples:
export const EXTENSION_EXAMPLES = {
  newChapter: { id: 3, name: 'Новая глава', next: null },
  newNpc: { id: 'archivist', name: 'Архивариус Кель', tone: 'холодный' },
  newDialogueNode: { dialogueId: 'neraFirst', nodeId: 'trust', speaker: 'Нера', text: 'Хорошо. Проверим твою волю.' },
  newItem: { id: 'starSalt', name: 'Звездная соль', type: 'craft' },
  newQuest: { id: 'q3_side_map', title: 'Потерянная карта', objectives: ['Найти карту'] },
  newAbility: { id: 'gravityWell', name: 'Гравитационный Колодец', dmg: 48, mana: 22, cooldown: 9 }
};
