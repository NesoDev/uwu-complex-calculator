<template>
    <div class="editor-container">
        <div class="code-wrapper">
            <div class="line-numbers" ref="lineNumbers">
                <div v-for="(_, index) in codeArray" :key="index">{{ index + 1 }}</div>
            </div>
            <textarea class="code-editor" :id="props.editable ? 'input-editor' : 'output-editor'" v-model="codeString"
                :readonly="currentMode === 'viewer'" @click="activateEditor" @keydown="handleKeyPress"
                @scroll="syncScroll" @input="emitCode">
            </textarea>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, computed, watch } from 'vue'
import { useStore } from 'vuex';

const props = defineProps({
    code: {
        type: String,
        require: true
    },
    editable: {
        type: Boolean,
        require: true
    }
})

const store = useStore()

const emits = defineEmits(['update:code'])

const emitCode = () => {
    emits("update:code", codeString.value);
}

const activateEditor = (event) => {
    if (props.editable) {
        currentMode.value = 'coder';
        event.target.focus();
    } else {
        event.target.blur();
    }
}

const currentMode = ref('viewer')
const codeString = ref(props.code)

const handleKeyPress = (event) => {
    const textarea = event.target
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const value = textarea.value


    if (props.editable) {
        if (event.key === 'Tab') {
            event.preventDefault()
            textarea.value = value.substring(0, start) + '    ' + value.substring(end);
            textarea.selectionStart = textarea.selectionEnd = start + 4;
        }

        if (event.key === 'Backspace') {
            if (start === end && start > 0) {
                const previousChar = value[start - 1]
                if (previousChar === ' ' && value.substring(start - 4, start) === '    ') {
                    event.preventDefault()
                    textarea.value = value.substring(0, start - 4) + value.substring(end)
                    textarea.selectionStart = textarea.selectionEnd = start - 4
                }
            }
        }
    }
}

//const codeLines = computed(() => {
//    return codeString.value.split('\n')
//})
const codeArray = computed(() => {
    let array = []
    let codeLines = codeString.value.split('\n')
    codeLines.forEach((codeLine) => {
        let groups = codeLine.match(/^( +)/)
        let tabs = groups ? groups[1].length : 0
        tabs = tabs / 4
        let object = { tabs: tabs, code: codeLine }
        array.push(object)
    })
    return array
})

const syncScroll = (event) => {
    const textarea = event.target
    const lineNumbers = document.querySelector('.line-numbers')
    if (lineNumbers) {
        lineNumbers.scrollTop = textarea.scrollTop
    }
}

watch(() => store.state.outputCode, () => {
    if (!props.editable) {
        console.log("Outputcode cambió")
        let newCode = store.state.outputCode
        codeString.value = newCode.slice(1, -1).replace(/\\n/g, '\n');
    }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&display=swap');

.editor-container {
    position: absolute;
    width: 100%;
    height: 100%;
    display: flex;
    overflow: scroll;
}

.code-wrapper {
    display: flex;
    width: 100%;
    height: 100%;
    overflow: auto;
}

.line-numbers {
    width: 21px;
    text-align: right;
    padding-right: 10px;
    color: #bf95ff;
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    user-select: none;
    overflow-y: auto;
    height: 100%;
    user-select: none;
    pointer-events: none;
}

.code-editor {
    flex-grow: 1;
    background: none;
    resize: none;
    outline: none;
    border: none;
    color: rgb(236, 236, 236);
    font-family: 'Fira Code', monospace;
    font-size: 14px;
    padding-left: 10px;
    overflow: auto;
    height: 100%;
    caret-color: #bf95ff
}

.code-editor::-webkit-scrollbar {
    display: none;
}

.line-numbers::-webkit-scrollbar {
    display: none;
}
</style>