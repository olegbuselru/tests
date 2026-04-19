# Echoes of the Rift — Browser RPG Vertical Slice

## Concept overview
Original single-player isekai-fantasy RPG vertical slice: герой погибает в современном мире, проходит метафизический переход и просыпается в мире магии, где “Эхо Мира” ведет его через классовый выбор, моральные дилеммы, спутника и раскрытие тайны руин.

## Architecture plan
- **Core systems:** bootstrap (`src/main.js`), main loop, scene manager, state manager, input, audio, save abstraction, event bus.
- **Gameplay systems:** player stats/progression, combat, dialogue, quests, inventory, world interactions.
- **Content systems:** data-driven registries in `src/content/data.js`.
- **Rendering/UI:** Canvas world rendering + layered HTML UI panels.

## File tree
- `index.html`
- `styles.css`
- `src/main.js`
- `src/core/EventBus.js`
- `src/core/StateManager.js`
- `src/core/InputManager.js`
- `src/core/AudioManager.js`
- `src/core/SaveManager.js`
- `src/core/SceneManager.js`
- `src/systems/StatsSystem.js`
- `src/systems/InventorySystem.js`
- `src/systems/QuestSystem.js`
- `src/systems/DialogueSystem.js`
- `src/systems/CombatSystem.js`
- `src/scenes/CinematicScene.js`
- `src/scenes/WorldScene.js`
- `src/ui/UIManager.js`
- `src/content/data.js`

## What is implemented
- Title screen with New Game / Continue / Settings.
- Intro cinematic with death + transition.
- Class selection: мечник / маг / следопыт.
- Chapter 1 gameplay: movement, dialogue with Nera, class skill combat, moral altar choice, chapter hook.
- Chapter 2 gameplay: village NPCs, branching reaction to Chapter 1 choice, 2 side quests, boss encounter, chapter end.
- Systems for HP/mana/XP/level, inventory, quests, dialogue choices, enemy AI, cooldowns, save-in-memory.
- HUD, quest journal, inventory panel, pause, death screen, chapter screen.

## Expansion points
In `src/content/data.js` section `EXTENSION_EXAMPLES`:
- add chapter (`newChapter`)
- add NPC (`newNpc`)
- add dialogue node (`newDialogueNode`)
- add item (`newItem`)
- add quest (`newQuest`)
- add class ability (`newAbility`)

## Run
Use any static web server from project root, for example:
```bash
python3 -m http.server 8000
```
Then open `http://localhost:8000`.

## Story map
- **Prologue:** Death in modern world → liminal dialogue with Echo.
- **Chapter I:** Awakening at shrine, meet Nera, first fights, altar moral choice.
- **Transition:** Night march to village edge.
- **Chapter II:** Village + ruins + tower, side quests, boss warden, core shard reveal, new rift cliffhanger.

## Entities table
### Classes
- Клинок Рассвета
- Эфирный Арканист
- Теневой Следопыт

### NPC
- Нера Пепельная
- Староста Орвейн
- Мила Травница

### Enemies
- Мшистый клык
- Пустотный разведчик
- Страж Реликтовой Башни (boss)

### Items
- Лунная трава
- Осколок Сердца Руин
- Железный оберег Милы

### Quests
- Голос в корнях (main ch1)
- Сердце Руин (main ch2)
- Тихие листья (side ch2)
- Следы в тумане (side ch2)

## Systems interaction scheme
`Input -> WorldScene -> Combat/Interaction -> Quest/Inventory/Stats -> UI`

`SceneManager <-> CinematicScene / WorldScene`

`DialogueSystem -> State flags/relationships -> Branches in WorldScene`

`SaveManager` stores whole `StateManager.state` snapshot in session memory.

## Dialogues, cutscenes, chapter switching
- Dialogues: graph nodes (`speaker`, `text`, `choices`, `next`, side effects) in `DIALOGUES` and interpreted by `DialogueSystem`.
- Cutscenes: timed text scenes in `CinematicScene`, skippable via Space.
- Chapter flow: `Game.progressChapter()` routes `chapter1 -> transition -> chapter2 -> chapter-end`.
