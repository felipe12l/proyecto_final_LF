<script setup>
import { ref } from 'vue'
import JWTAnalyzer from './components/JWTAnalyzer.vue'
import JWTEncoder from './components/JWTEncoder.vue'

const activeTab = ref('analyze')
</script>

<template>
  <div class="app-container">
    <header>
      <h1> JWT Analyzer</h1>
      <p>Analizador y generador de JSON Web Tokens</p>
    </header>

    <div class="tabs">
      <button 
        :class="{ active: activeTab === 'analyze' }" 
        @click="activeTab = 'analyze'"
      >
        Analizar JWT
      </button>
      <button 
        :class="{ active: activeTab === 'encode' }" 
        @click="activeTab = 'encode'"
      >
        Generar JWT
      </button>
    </div>

    <div class="tab-content">
      <JWTAnalyzer v-if="activeTab === 'analyze'" />
      <JWTEncoder v-if="activeTab === 'encode'" />
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

.app-container {
  max-width: 1200px;
  margin: 0 auto;
}

header {
  text-align: center;
  color: white;
  margin-bottom: 30px;
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  justify-content: center;
}

.tabs button {
  padding: 12px 30px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s;
}

.tabs button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.tabs button.active {
  background: white;
  color: #667eea;
  font-weight: 600;
}

.tab-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}
</style>
