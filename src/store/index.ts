import { createStore } from 'vuex'
const backendUrl = "https://uwu-complex-calculator.onrender.com"
const openaiUrl = "https://api.openai.com/v1/chat/completions"
const openaiApiKey = process.env.VUE_APP_OPENAI_API_KEY
export default createStore({
  state: {
    evaluatingCode: false,
    outputCode: ""
  },
  getters: {
  },
  mutations: {
  },
  actions: {
    async evaluateCode(context, codeString: string) {
      try {
        console.log(`Enviando código al backend`)
        const response = await fetch(`${backendUrl}/analyze`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ code: codeString })
        })
        const data = await response.json();
        console.log(`Response Backend: ${JSON.stringify(data)}`)
        return data
      }
      catch (err) {
        console.log('[ERROR] Falló la conexión con el servidor')
        console.error(err)
      }
    },

    async improveCode(context, codeString) {
      try {
        console.log(`Enviando código a OpenAI`);
        const response = await fetch(`${openaiUrl}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${openaiApiKey}`
          },
          body: JSON.stringify({
            model: 'gpt-3.5-turbo',
            messages: [
              {
                role: "system",
                content: `
                              Eres un asistente experto en optimización de código. 
                              Tu tarea es recibir un código en un lenguaje específico y mejorarlo según las siguientes reglas:
                              1. El código debe mantener la misma funcionalidad original.
                              2. Disminuye al maximo prosible, la complejidad computacional siempre que sea posible.
                              3. Retorna solamente código, no incluyas ningún tipo de contexto.
                              4. En ningún caso debes retornar otro tipo de texto que no sea código
                              5. Te recuerdo nuevamente que por ningún motivo retornes texto distinto a código
                              6. El código retornado debe estar en el mismo lenguaje pero formateado como un string con:
                                 - Saltos de línea representados por '\n'.
                                 - Tabulaciones representadas por 4 espacios consecutivos.
                              7. No utilices palabras reservadas que aumenten la complejidad por encima de O(n) o O(1).
                              8. Si el lenguaje es no tipado, no declares explícitamente el tipo de las variables.
                          `
              },
              { role: "user", content: `Optimiza el siguiente código:\n${codeString}` }
            ],
            max_tokens: 500,
          })
        });

        const data = await response.json();
        const content = data.choices[0].message.content;
        console.log(`Response openai: ${JSON.stringify(content)}`);
        return content;
      } catch (err) {
        console.log('[ERROR] Falló la conexión con openai');
        console.error(err);
      }
    }
  },
  modules: {
  }
})
