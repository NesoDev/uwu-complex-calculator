<template>
  <div id="home">
    <div class="section-home" id="first-section">
      <div class="head">
        <DropDown id="dropdown" :options="options" :optionDefault="{ path: '', text: 'Select a language' }"
          @update:option="updateLanguage" />
        <button id="evaluate" class="head-button" @click="processCode" @update:code="inputCode">
          <img src="@/assets/icon-play.png" alt="play-icon" width="14" height="14">
          <p>Evaluate</p>
        </button>
      </div>
      <hr>
      <div class="section-code">
        <CodeEditor :editable="true" :code="inputCode" @update:code="updateInputCode" />
      </div>
      <hr>
      <div class="foot">
        <div class="tag-foot">
          <img src="@/assets/icon-time.png" alt="">
          <span>Complex: {{ complexInput }}</span>
        </div>
        <button id="show-graph-input" class="foot-button" @click="showGraph(complexInput)">
          <img src="@/assets/icon-graph.png" alt="icon-graph">
          <p>Show graph</p>
        </button>
      </div>
    </div>
    <div class="section-home" id="second-section">
      <div class="head">
        <div class="tag-head">
          <img src="@/assets/icon-trophy.png" alt="trophy-icon" width="18" height="18">
          <p> Improved code alternative </p>
        </div>
        <button id="copy" class="head-button" @click="copyCode">
          <img src="@/assets/icon-copy.png" alt="copy-icon" width="18" height="18">
          <p>Copy</p>
        </button>
      </div>
      <hr>
      <div class="section-code">
        <CodeEditor :editable="false" :code="outputCode" />
      </div>
      <hr>
      <div class="foot">
        <div class="tag-foot">
          <img src="@/assets/icon-time.png" alt="">
          <span>Complex: {{ complexOutput }}</span>
        </div>
        <button id="show-graph-output" class="foot-button" @click="showGraph(complexOutput)">
          <img src="@/assets/icon-graph.png" alt="icon-graph">
          <p>Show graph</p>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useStore } from 'vuex';
import DropDown from '@/components/DropDown.vue';
import CodeEditor from '@/components/CodeEditor.vue';

const options = [
  { text: "Python", path: "https://res.cloudinary.com/dozfohnhs/image/upload/v1732400694/Python_rnzhsv.png" },
  { text: "JavaScript", path: "https://res.cloudinary.com/dozfohnhs/image/upload/v1732425450/JavaScript_odeoky.png" },
  { text: "Java", path: "https://res.cloudinary.com/dozfohnhs/image/upload/v1732425450/Java_hteqf4.png" },
  { text: "Swift", path: "https://res.cloudinary.com/dozfohnhs/image/upload/v1732425450/Swift_cmwm5n.png" },
]
const language = ref("")
const inputCode = ref("for i in range(n):\n    pass")
const outputCode = ref("")
const complexInput = ref(" - - ")
const complexOutput = ref("")

const updateLanguage = (newLanguage) => {
  language.value = newLanguage
}

const updateInputCode = (code) => {
  inputCode.value = code
}

const store = useStore()

const processCode = async () => {
  if (language.value) {
    complexInput.value = ""
    // calculamos la complejidad del código ingresado
    let res = await store.dispatch('evaluateCode', inputCode.value)
    console.log(`Response Backend: ${JSON.stringify(res)}`)
    if (res.success) {
      complexInput.value = res.complexity
      // obtenemos un código obtimizado
      outputCode.value = await store.dispatch('improveCode', inputCode.value)
      store.state.outputCode = outputCode.value

      // calculamos la complejidad del código obtenido
      complexOutput.value = ""
      res = await store.dispatch('evaluateCode', outputCode.value)
      console.log(`Response Backend: ${JSON.stringify(res)}`)
      if (res.success) {
        complexOutput.value = res.complexity
      } else {
        alert(`Error! Incorrect ${language.value} syntax`)
      }
    } else {
      alert(`Error! Incorrect ${language.value} syntax`)
    }
  } else {
    alert("Warning! Don't language select")
  }
}

</script>

<style scoped>
#home {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-home {
  width: 100%;
  height: 100%;
  background: #0f0b1e;
  border-radius: 20px;
  padding: 10px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1px solid #151124;
}

#first-section {
  grid-area: input-code;
  grid-template-rows: auto auto 1fr;
  row-gap: 10px;
}

.head {
  width: 100%;
  height: 40px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 10px;
  z-index: 1;
}

#dropdown {
  width: 65%;
}

.head-button,
.foot-button {
  border: none;
  height: 100%;
  padding: 15px;
  box-sizing: border-box;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  gap: 5px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  font-family: "Fira Code", monospace;
  transition: background 0.3s ease-out;
  cursor: pointer;
}

#evaluate {
  width: 35%;
  max-width: 130px;
  background: #1b984d;
  color: #c0e8d0;
}

#evaluate:hover {
  background: #34988c;
}

hr {
  height: 0;
  border: 1px solid #171333;
}

.section-code {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.foot {
  width: 100%;
  height: 40px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 10px;
}

.tag-foot {
  height: 100%;
  width: auto;
  box-sizing: border-box;
  padding: 15px;
  border-radius: 4px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  color: #4d4e9e;
  font-size: 13px;
  font-weight: 700;
  font-family: "Fira Code", monospace;
  gap: 10px;
}

#show-graph-input,
#show-graph-output {
  background: #261a5a;
  color: #a9a0cf
}

/*  */

#second-section {
  grid-area: output-code;
  grid-template-rows: auto auto 1fr;
  row-gap: 10px;
}

.tag-head {
  height: 100%;
  width: auto;
  background: #1a163a;
  box-sizing: border-box;
  padding: 15px;
  border-radius: 10px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  color: #cdcbea;
  font-size: 13px;
  font-weight: 700;
  font-family: "Fira Code", monospace;
  gap: 10px;
}

#copy {
  background: #1a163a;
  color: #a9a0cf
}
</style>