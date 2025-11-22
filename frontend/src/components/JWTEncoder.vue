<script setup>
import { ref } from 'vue'

const header = ref({
  alg: 'HS256',
  typ: 'JWT'
})

const payload = ref({
  sub: '1234567890',
  name: 'John Doe',
  iat: Math.floor(Date.now() / 1000)
})

const secret = ref('your-secret-key')
const loading = ref(false)
const result = ref(null)
const error = ref(null)

const encodeToken = async () => {
  loading.value = true
  error.value = null
  result.value = null

  try {
    const response = await fetch('/api/encode', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        header: header.value,
        payload: payload.value,
        secret: secret.value
      })
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Error al generar el token')
    }

    result.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const clearForm = () => {
  header.value = { alg: 'HS256', typ: 'JWT' }
  payload.value = { sub: '1234567890', name: 'John Doe', iat: Math.floor(Date.now() / 1000) }
  secret.value = 'your-secret-key'
  result.value = null
  error.value = null
}

const copyToken = () => {
  if (result.value?.token) {
    navigator.clipboard.writeText(result.value.token)
    alert('Token copiado al portapapeles')
  }
}

const addPayloadField = () => {
  const key = prompt('Nombre del campo:')
  if (key && key.trim()) {
    const value = prompt('Valor del campo:')
    payload.value[key.trim()] = value || ''
  }
}
</script>

<template>
  <div class="encoder-container">
    <h2>Generar Token JWT</h2>
    <p class="description">Crea un nuevo token JWT configurando el header, payload y secreto</p>

    <div class="form-row">
      <div class="form-group">
        <label for="header">Header (JSON):</label>
        <textarea
          id="header"
          v-model="header.alg"
          placeholder="Algoritmo"
          rows="1"
          :disabled="loading"
        ></textarea>
        <select v-model="header.alg" :disabled="loading" class="select-input">
          <option value="HS256">HS256</option>
          <option value="HS384">HS384</option>
          <option value="HS512">HS512</option>
          <option value="RS256">RS256</option>
        </select>
      </div>
    </div>

    <div class="form-group">
      <label>Payload:</label>
      <div class="payload-editor">
        <div v-for="(value, key) in payload" :key="key" class="payload-field">
          <input 
            type="text" 
            :value="key" 
            disabled 
            class="field-key"
          />
          <input 
            v-model="payload[key]" 
            type="text" 
            class="field-value"
            :disabled="loading"
          />
          <button 
            @click="delete payload[key]" 
            class="btn-delete"
            :disabled="loading"
          >
            ✕
          </button>
        </div>
        <button @click="addPayloadField" class="btn-add" :disabled="loading">
          + Agregar Campo
        </button>
      </div>
    </div>

    <div class="form-group">
      <label for="secret">Secreto:</label>
      <input
        id="secret"
        v-model="secret"
        type="text"
        placeholder="Ingresa tu clave secreta"
        :disabled="loading"
        class="text-input"
      />
    </div>

    <div class="button-group">
      <button @click="encodeToken" :disabled="loading" class="btn-primary">
        {{ loading ? 'Generando...' : 'Generar Token' }}
      </button>
      <button @click="clearForm" :disabled="loading" class="btn-secondary">
        Limpiar
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-error">
      <strong>Error:</strong> {{ error }}
    </div>

    <!-- Resultado -->
    <div v-if="result" class="result-container">
      <div class="success-badge">✓ Token generado</div>

      <div class="result-section">
        <div class="token-header">
          <h3>Token JWT</h3>
          <button @click="copyToken" class="btn-copy">📋 Copiar</button>
        </div>
        <div class="token-display">{{ result.token }}</div>
      </div>

      <div class="result-section" v-if="result.header">
        <h3>Header</h3>
        <pre>{{ JSON.stringify(result.header, null, 2) }}</pre>
      </div>

      <div class="result-section" v-if="result.payload">
        <h3>Payload</h3>
        <pre>{{ JSON.stringify(result.payload, null, 2) }}</pre>
      </div>

      <div class="result-section" v-if="result.signature">
        <h3>Signature</h3>
        <pre>{{ result.signature }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.encoder-container {
  max-width: 900px;
  margin: 0 auto;
}

h2 {
  color: #333;
  margin-bottom: 10px;
}

.description {
  color: #666;
  margin-bottom: 25px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

textarea, .text-input, .select-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  transition: border-color 0.3s;
}

textarea {
  font-family: 'Courier New', monospace;
  resize: vertical;
}

.text-input:focus, .select-input:focus, textarea:focus {
  outline: none;
  border-color: #667eea;
}

.select-input {
  background: white;
  cursor: pointer;
  margin-top: 8px;
}

.payload-editor {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
}

.payload-field {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.field-key {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #f0f0f0;
  font-weight: 600;
}

.field-value {
  flex: 2;
  padding: 10px;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
}

.field-value:focus {
  outline: none;
  border-color: #667eea;
}

.btn-delete {
  padding: 8px 12px;
  background: #ff6b6b;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-delete:hover:not(:disabled) {
  background: #ff5252;
}

.btn-add {
  width: 100%;
  padding: 10px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.3s;
}

.btn-add:hover:not(:disabled) {
  background: #5568d3;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover:not(:disabled) {
  background: #e0e0e0;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert {
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.alert-error {
  background: #fee;
  border: 1px solid #fcc;
  color: #c33;
}

.result-container {
  margin-top: 30px;
  animation: fadeIn 0.5s;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.success-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  margin-bottom: 20px;
  background: #d4edda;
  color: #155724;
}

.result-section {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.result-section h3 {
  color: #667eea;
  margin-bottom: 10px;
  font-size: 1.1rem;
}

.token-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.btn-copy {
  padding: 8px 16px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
}

.btn-copy:hover {
  background: #5568d3;
}

.token-display {
  background: #1e1e1e;
  color: #4ec9b0;
  padding: 15px;
  border-radius: 6px;
  word-break: break-all;
  font-family: 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.6;
}

pre {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 15px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.5;
}
</style>
