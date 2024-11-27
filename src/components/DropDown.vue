<template>
  <div class="dropdown">
        <div id="select" @click='selectClicked'>
            <span id="option-selected">
                <img :src="optionSelected.path" alt="">
                <p>{{ optionSelected.text }}</p>
            </span>
            <img class="caret" :class="{ 'rotate-left': menuOpen, 'rotate-right': menuClose }" src="@/assets/icon-arrow.png" alt="icon-arrow">
        </div>
        <Transition>
            <ul id="menu" v-if="menuOpen">
                <li v-for="(option, i) in options" :key="i">
                    <div class="option" @click="emitOption(option)">
                        <img :src="option.path" alt="icon-option">
                        <p>{{ option.text }}</p>
                    </div>
                    <hr v-if="i < options.length - 1"/>
                </li>
            </ul>
        </Transition>
    </div>
</template>

<script setup>
import {ref, defineProps, defineEmits, onMounted} from 'vue';
const props = defineProps({
    options: {
        type: Array,
        require: true
    },
    optionDefault: {
        type: Object,
        require: true
    }
})
const emits = defineEmits(["update:option"])
const selectElement = ref()
const menuOpen = ref(false);
const menuClose = ref(true)
const menuBlocked = ref(false);
const optionSelected = ref(props.optionDefault);

const selectClicked = () => {
    if (!menuBlocked.value) {
        menuOpen.value = !menuOpen.value;
        menuClose.value = !menuOpen.value
    }
}
const emitOption = (option) => {
    if (option.text != optionSelected.value.text) {
    optionSelected.value = option
        emits("update:option", option.text)
    }
}

onMounted(() => {
    selectElement.value = document.getElementById("select")
    document.addEventListener("click", (event) => {
        if (!selectElement.value.contains(event.target) && menuOpen.value) {
            console.log("cerrando menu")
            selectClicked()
        }
    })
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&display=swap');
.dropdown {
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 5px;
    box-sizing: border-box;
}

#select {
    width: 100%;
    height: 100%;
    background: #1a163a;
    padding: 15px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    border-radius: 10px;
    cursor: pointer;
}

.rotate-left {
    transform: rotate(180deg);
    transition: transform 0.5s ease-in-out;
}

.rotate-right {
    transform: rotate(0deg);
    transition: transform 0.5s ease-in-out;
}

#option-selected {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-evenly;
    gap: 8px;
    font-size: 12px;
    font-weight: 500;
    font-family: "Fira Code", monospace;
    color: #d2d1e6;
}

#menu {
    width: 100%;
    height: auto;
    background: #1a163a;
    border-radius: 10px;
    padding: 8px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    box-sizing: border-box;
}

#menu li {
    width: 100%;
    height: auto;
    display: flex;
    flex-direction: column;
    gap: 5px;
}

li .option {
    width: 100%;
    height: auto;
    padding: 5px;
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 8px;
    cursor: pointer;
}

#menu li hr {
    border: 1px solid #1f1943;
}

.option p {
    font-size: 12px;
    font-weight: 500;
    font-family: "Fira Code", monospace;
    color: #d0d4f9;
    text-overflow: ellipsis;
}

.option:hover {
    background: #251f54;
}

.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease-out, transform 0.2s ease-out;
}

.v-enter-from {
  opacity: 0;
  transform: scale(0.8); /* Tamaño inicial reducido */
}

.v-enter-to {
  opacity: 1;
  transform: scale(1); /* Tamaño normal */
}

.v-leave-from {
  opacity: 1;
  transform: scale(1); /* Tamaño normal */
}

.v-leave-to {
  opacity: 0;
  transform: scale(0.8); /* Tamaño reducido */
}
</style>