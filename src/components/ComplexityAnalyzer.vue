<template>
  <div class="complexity-analyzer">
    <h2>Analizador de Complejidad de Funciones Python</h2>
    <div class="code-input">
      <textarea
        v-model="code"
        placeholder="Ingrese su función Python aquí..."
        rows="10"
      ></textarea>
    </div>
    <button @click="analyzeCode" :disabled="!code">Analizar Complejidad</button>
    
    <div v-if="result" class="result">
      <h3>Resultado del Análisis:</h3>
      <p>Complejidad: <strong>{{ result.complexity }}</strong></p>
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'ComplexityAnalyzer',
  data() {
    return {
      code: '',
      result: null,
      error: null
    }
  },
  methods: {
    async analyzeCode() {
      try {
        this.error = null;
        this.result = null;
        
        const response = await fetch('http://localhost:5000/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ code: this.code })
        });

        const data = await response.json();
        
        if (data.success) {
          this.result = data;
        } else {
          this.error = data.error || 'Error al analizar el código';
        }
      } catch (err) {
        this.error = 'Error de conexión con el servidor';
        console.error(err);
      }
    }
  }
}
</script>

<style scoped>
.complexity-analyzer {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.code-input {
  margin: 20px 0;
}

textarea {
  width: 100%;
  padding: 10px;
  font-family: monospace;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

.result {
  margin-top: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.error {
  margin-top: 20px;
  padding: 15px;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 4px;
}
</style>
