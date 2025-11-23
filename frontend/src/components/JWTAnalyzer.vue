<script setup>
import { ref } from 'vue'
import DerivationTree from './DerivationTree.vue'

const token = ref('')
const loading = ref(false)
const result = ref(null)
const error = ref(null)

const analyzeToken = async () => {
  if (!token.value.trim()) {
    error.value = 'Por favor ingresa un token JWT'
    return
  }

  loading.value = true
  error.value = null
  result.value = null

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token: token.value })
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Error al analizar el token')
    }

    result.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const clearForm = () => {
  token.value = ''
  result.value = null
  error.value = null
}

const loadSampleToken = () => {
  token.value = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
}
</script>

<template>
  <div class="analyzer-container">
    <h2>Analizar Token JWT</h2>
    <p class="description">Pega tu token JWT para analizar su estructura, validez y contenido</p>

    <div class="form-group">
      <label for="token">Token JWT:</label>
      <textarea
        id="token"
        v-model="token"
        placeholder="Pega tu token JWT aquí..."
        rows="6"
        :disabled="loading"
      ></textarea>
    </div>

    <div class="button-group">
      <button @click="analyzeToken" :disabled="loading" class="btn-primary">
        {{ loading ? 'Analizando...' : 'Analizar Token' }}
      </button>
      <button @click="loadSampleToken" :disabled="loading" class="btn-secondary">
        Cargar Ejemplo
      </button>
      <button @click="clearForm" :disabled="loading" class="btn-secondary">
        Limpiar
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-error">
      <strong>Error:</strong> {{ error }}
    </div>

    <!-- Resultado exitoso -->
    <div v-if="result && result.status === 'ok'" class="result-container">
      <div class="success-badge">✓ Análisis completado</div>

      <div class="result-section">
        <h3>Header</h3>
        <pre>{{ JSON.stringify(result.header, null, 2) }}</pre>
      </div>

      <div class="result-section">
        <h3>Payload</h3>
        <pre>{{ JSON.stringify(result.payload, null, 2) }}</pre>
      </div>

      <div class="result-section">
        <h3>Signature</h3>
        <pre>{{ result.signature }}</pre>
      </div>

      <div class="result-section" v-if="result.tokens">
        <h3>Tokens Léxicos</h3>
        <details>
          <summary>Token Codificado ({{ result.tokens.encoded?.length || 0 }} tokens)</summary>
          <pre>{{ JSON.stringify(result.tokens.encoded, null, 2) }}</pre>
        </details>
        <details>
          <summary>Header ({{ result.tokens.header?.length || 0 }} tokens)</summary>
          <pre>{{ JSON.stringify(result.tokens.header, null, 2) }}</pre>
        </details>
        <details>
          <summary>Payload ({{ result.tokens.payload?.length || 0 }} tokens)</summary>
          <pre>{{ JSON.stringify(result.tokens.payload, null, 2) }}</pre>
        </details>
      </div>

      <!-- Árbol de Derivaciones -->
      <DerivationTree v-if="result.derivation_tree" :tree="result.derivation_tree" />
    </div>

    <!-- Resultado con error -->
    <div v-if="result && result.status === 'error'" class="result-container error-result">
      <div class="error-badge">✗ Error en el análisis</div>
      <div class="result-section">
        <h3>Fase: {{ result.phase }}</h3>
        <p class="error-message">{{ result.message }}</p>
        <pre v-if="result.header">Header: {{ JSON.stringify(result.header, null, 2) }}</pre>
        <pre v-if="result.payload">Payload: {{ JSON.stringify(result.payload, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.analyzer-container {
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

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 8px;
  color: #333;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  resize: vertical;
  transition: border-color 0.3s;
}

textarea:focus {
  outline: none;
  border-color: #667eea;
}

textarea:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
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

.success-badge, .error-badge {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  margin-bottom: 20px;
}

.success-badge {
  background: #d4edda;
  color: #155724;
}

.error-badge {
  background: #f8d7da;
  color: #721c24;
}

.result-section {
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 15px;
  border: 1px solid #e0e0e0;
}

.result-section h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.1rem;
  font-weight: 700;
}

pre {
  background: #f5f5f5;
  color: #222;
  padding: 15px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.5;
  border: 1px solid #ddd;
}

details {
  margin-top: 10px;
  cursor: pointer;
}

summary {
  font-weight: 600;
  padding: 10px;
  color: #667eea;
  background: white;
  border-radius: 6px;
  margin-bottom: 10px;
}

summary:hover {
  background: #f0f0f0;
  color: #667eea;
}

.error-message {
  color: #c33;
  font-weight: 600;
  margin-bottom: 10px;
}

.error-result {
  border-left: 4px solid #c33;
}
</style>
