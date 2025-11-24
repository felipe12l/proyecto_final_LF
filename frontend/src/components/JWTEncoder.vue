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
const testCases = ref(null)
const loadingTests = ref(false)
const testResults = ref(null)
const loadingTestResults = ref(false)

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
  const text = result.value?.jwt;
  if (!text) return;

  // Método moderno (solo funciona en HTTPS)
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text)
      .then(() => alert("Token copiado al portapapeles"))
      .catch(() => fallbackCopy(text));
  } else {
    // Fallback para HTTP (como tu servidor de AWS)
    fallbackCopy(text);
  }
};

const fallbackCopy = (text) => {
  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.style.position = "fixed";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
  alert("Token copiado al portapapeles");
};

const numericClaims = ["iat", "exp", "nbf"]

const addPayloadField = () => {
  const key = prompt('Nombre del campo:')
  if (!key || !key.trim()) return

  const raw = prompt('Valor del campo:')
  let value = raw

  if (numericClaims.includes(key.trim())) {
    const num = Number(raw)
    value = isNaN(num) ? raw : num
  }

  payload.value[key.trim()] = value
}

const loadTestCases = async () => {
  loadingTests.value = true
  error.value = null

  try {
    const response = await fetch('/api/get_encoded_tests', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Error al cargar los casos de prueba')
    }

    testCases.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    loadingTests.value = false
  }
}

const runEncoderTests = async () => {
  loadingTestResults.value = true
  error.value = null
  testResults.value = null

  try {
    const response = await fetch('/api/test_encode_all', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || 'Error al ejecutar las pruebas')
    }

    testResults.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    loadingTestResults.value = false
  }
}

const loadTestCase = (testCase) => {
  header.value = testCase.header
  payload.value = testCase.payload
  secret.value = testCase.secret || 'your-secret-key'
}

const truncateToken = (tokenStr) => {
  if (!tokenStr) return 'N/A'
  return tokenStr.length > 50 ? tokenStr.substring(0, 50) + '...' : tokenStr
}

const numericClaims = ["iat", "exp", "nbf"]

function convertField(key) {
  if (numericClaims.includes(key)) {
    const val = payload.value[key]
    const num = Number(val)
    if (!isNaN(num)) {
      payload.value[key] = num
    }
  }
}
</script>

<template>
  <div class="encoder-container">
    <h2>Generar Token JWT</h2>
    <p class="description">Crea un nuevo token JWT configurando el header, payload y secreto</p>

    <div class="form-row">
      <div class="form-group">
        <label for="algorithm">Algoritmo:</label>
        <select v-model="header.alg" :disabled="loading" class="select-input">
          <option value="HS256">HS256</option>
          <option value="HS384">HS384</option>
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
            @input="convertField(key)"
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
      <button @click="loadTestCases" :disabled="loadingTests" class="btn-secondary">
        {{ loadingTests ? 'Cargando...' : 'Ver Casos de Prueba' }}
      </button>
      <button @click="runEncoderTests" :disabled="loadingTestResults" class="btn-secondary">
        {{ loadingTestResults ? 'Ejecutando...' : 'Ejecutar Pruebas' }}
      </button>
      <button @click="clearForm" :disabled="loading" class="btn-secondary">
        Limpiar
      </button>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-error">
      <strong>Error:</strong> {{ error }}
    </div>

    <!-- Resultados de Pruebas -->
    <div v-if="testResults" class="test-results-container">
      <h3>Resultados de Pruebas de Encoding</h3>
      <div class="summary-stats">
        <div class="stat-card stat-total">
          <div class="stat-number">{{ testResults.summary?.total || 0 }}</div>
          <div class="stat-label">Total</div>
        </div>
        <div class="stat-card stat-passed">
          <div class="stat-number">{{ testResults.summary?.passed || 0 }}</div>
          <div class="stat-label">Exitosas</div>
        </div>
        <div class="stat-card stat-failed">
          <div class="stat-number">{{ testResults.summary?.failed || 0 }}</div>
          <div class="stat-label">Fallidas</div>
        </div>
      </div>

      <div class="table-wrapper">
        <table class="test-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Estado</th>
              <th>Algoritmo</th>
              <th>Mensaje</th>
              <th>Match</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(testResult, index) in testResults.results" :key="index">
              <td>{{ index + 1 }}</td>
              <td>
                <span 
                  class="badge" 
                  :class="testResult.status === 'ok' ? 'badge-success' : 'badge-error'"
                >
                  {{ testResult.status === 'ok' ? '✓ OK' : '✗ Error' }}
                </span>
              </td>
              <td>
                <span class="badge badge-algo">{{ testResult.algorithm || testResult.header?.alg || 'N/A' }}</span>
              </td>
              <td class="message-cell">{{ testResult.message || 'N/A' }}</td>
              <td>
                <span 
                  v-if="testResult.match !== undefined"
                  class="badge" 
                  :class="testResult.match ? 'badge-success' : 'badge-warning'"
                >
                  {{ testResult.match ? '✓ Coincide' : '⚠ Difiere' }}
                </span>
                <span v-else class="text-muted">-</span>
              </td>
              <td>
                <button 
                  v-if="testResult.header && testResult.payload"
                  @click="loadTestCase(testResult)" 
                  class="btn-small"
                  title="Cargar este caso"
                >
                  Cargar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tabla de Casos de Prueba -->
    <div v-if="testCases" class="test-cases-container">
      <h3>Casos de Prueba de Tokens Encriptados</h3>
      <p class="test-info">Total de tokens: {{ testCases.total || 0 }}</p>
      
      <div class="table-wrapper">
        <table class="test-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Algoritmo</th>
              <th>Token JWT</th>
              <th>Payload</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(test, index) in testCases.results" :key="index">
              <td>{{ index + 1 }}</td>
              <td>
                <span class="badge badge-algo">{{ test.header?.alg || 'N/A' }}</span>
              </td>
              <td class="token-cell">
                <code>{{ truncateToken(test.jwt) }}</code>
              </td>
              <td class="payload-cell">
                <code>{{ JSON.stringify(test.payload).substring(0, 30) }}...</code>
              </td>
              <td>
                <button 
                  @click="loadTestCase(test)" 
                  class="btn-small"
                  title="Cargar este caso"
                >
                  Cargar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Resultado -->
    <div v-if="result" class="result-container">
      <div class="success-badge">✓ Token generado</div>

      <div class="result-section">
        <div class="token-header">
          <h3>Token JWT</h3>
          <button @click="copyToken" class="btn-copy">📋 Copiar</button>
        </div>
        <div class="token-display">{{ result.jwt }}</div>
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
  padding: 0 15px;
}

h2 {
  color: #333;
  margin-bottom: 10px;
  font-size: clamp(1.5rem, 4vw, 2rem);
}

.description {
  color: #666;
  margin-bottom: 25px;
  font-size: clamp(0.875rem, 2vw, 1rem);
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
  font-size: clamp(0.875rem, 2vw, 1rem);
}

textarea, .select-input {
  color:#222;
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: clamp(0.875rem, 2vw, 1rem);
  transition: border-color 0.3s;
  box-sizing: border-box;
}
.text-input{
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: clamp(0.875rem, 2vw, 1rem);
  transition: border-color 0.3s;
  box-sizing: border-box;
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
  flex-wrap: wrap;
}

.field-key {
  flex: 1;
  min-width: 120px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #f0f0f0;
  font-weight: 600;
  font-size: clamp(0.875rem, 2vw, 1rem);
}

.field-value {
  flex: 2;
  min-width: 150px;
  padding: 10px;
  border: 2px solid #e0e0e0;
  border-radius: 6px;
  font-size: clamp(0.875rem, 2vw, 1rem);
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
  white-space: nowrap;
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
  font-size: clamp(0.875rem, 2vw, 1rem);
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
  font-size: clamp(0.875rem, 2vw, 1rem);
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  flex: 1;
  min-width: 140px;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
  flex: 1;
  min-width: 120px;
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
  background: #ffffff;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  border: 1px solid #e0e0e0;
}

.result-section h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: clamp(1rem, 2.5vw, 1.1rem);
  font-weight: 700;
}

.token-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  flex-wrap: wrap;
  gap: 10px;
}

.btn-copy {
  padding: 8px 16px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  white-space: nowrap;
}

.btn-copy:hover {
  background: #5568d3;
}

.token-display {
  background: #f5f5f5;
  color: #2c5282;
  padding: 15px;
  border-radius: 6px;
  word-break: break-all;
  font-family: 'Courier New', monospace;
  font-size: clamp(0.75rem, 2vw, 0.875rem);
  line-height: 1.6;
  border: 1px solid #ddd;
}

pre {
  background: #f5f5f5;
  color: #222;
  padding: 15px;
  border-radius: 6px;
  overflow-x: auto;
  font-size: clamp(0.75rem, 2vw, 0.875rem);
  line-height: 1.5;
  border: 1px solid #ddd;
}

/* Estilos para la tabla de casos de prueba */
.test-cases-container, .test-results-container {
  margin-top: 30px;
  padding: 15px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.test-cases-container h3, .test-results-container h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: clamp(1rem, 2.5vw, 1.2rem);
}

.test-info {
  color: #666;
  margin-bottom: 15px;
  font-size: clamp(0.875rem, 2vw, 0.95rem);
}

/* Estilos para las estadísticas de pruebas */
.summary-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  border: 2px solid;
}

.stat-total {
  background: #e3f2fd;
  border-color: #2196f3;
}

.stat-passed {
  background: #e8f5e9;
  border-color: #4caf50;
}

.stat-failed {
  background: #ffebee;
  border-color: #f44336;
}

.stat-number {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: 700;
  margin-bottom: 5px;
}

.stat-total .stat-number {
  color: #2196f3;
}

.stat-passed .stat-number {
  color: #4caf50;
}

.stat-failed .stat-number {
  color: #f44336;
}

.stat-label {
  font-size: clamp(0.875rem, 2vw, 1rem);
  font-weight: 600;
  color: #666;
}

.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.test-table {
  width: 100%;
  min-width: 600px;
  border-collapse: collapse;
  font-size: clamp(0.75rem, 2vw, 0.9rem);
}

.test-table thead {
  background: #f8f9fa;
}

.test-table th {
  padding: 10px 8px;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #dee2e6;
  white-space: nowrap;
}

.test-table td {
  padding: 10px 8px;
  border-bottom: 1px solid #e9ecef;
  color: #333;
  vertical-align: middle;
}

.test-table tbody tr:hover {
  background: #f8f9fa;
}

.token-cell, .payload-cell, .message-cell {
  max-width: 200px;
  word-break: break-all;
}

.token-cell code, .payload-cell code {
  background: #f5f5f5;
  padding: 4px 8px;
  border-radius: 3px;
  font-size: clamp(0.7rem, 1.8vw, 0.85rem);
  color: #222;
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
}

.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: clamp(0.7rem, 1.8vw, 0.8rem);
  font-weight: 600;
  text-transform: uppercase;
  display: inline-block;
  white-space: nowrap;
}

.badge-algo {
  background: #e3f2fd;
  color: #1976d2;
}

.badge-success {
  background: #d4edda;
  color: #155724;
}

.badge-error {
  background: #f8d7da;
  color: #721c24;
}

.badge-warning {
  background: #fff3cd;
  color: #856404;
}

.text-muted {
  color: #999;
}

.btn-small {
  padding: 6px 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: clamp(0.75rem, 2vw, 0.85rem);
  transition: background 0.3s;
  white-space: nowrap;
}

.btn-small:hover {
  background: #764ba2;
}

/* Media Queries para Responsive */
@media (max-width: 768px) {
  .encoder-container {
    padding: 0 10px;
  }
  
  .payload-field {
    flex-direction: column;
  }
  
  .field-key, .field-value {
    min-width: 100%;
  }
  
  .button-group {
    flex-direction: column;
  }
  
  .btn-primary, .btn-secondary {
    width: 100%;
    min-width: 100%;
  }
  
  .token-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .btn-copy {
    width: 100%;
  }
  
  .test-table {
    min-width: 500px;
  }
  
  .test-table th,
  .test-table td {
    padding: 8px 6px;
  }
}

@media (max-width: 480px) {
  .test-cases-container {
    padding: 10px;
  }
  
  .result-section {
    padding: 12px;
  }
  
  .test-table {
    min-width: 450px;
    font-size: 0.75rem;
  }
  
  .token-cell, .payload-cell {
    max-width: 150px;
  }
}
</style>
