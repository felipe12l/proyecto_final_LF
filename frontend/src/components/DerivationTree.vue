<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  tree: {
    type: Object,
    required: true
  }
})

const expandedNodes = ref(new Set())

const toggleNode = (nodeId) => {
  if (expandedNodes.value.has(nodeId)) {
    expandedNodes.value.delete(nodeId)
  } else {
    expandedNodes.value.add(nodeId)
  }
}

const isExpanded = (nodeId) => {
  return expandedNodes.value.has(nodeId)
}

const expandAll = () => {
  const allIds = new Set()
  const collectIds = (node, path = '') => {
    const id = path || 'root'
    allIds.add(id)
    if (node.children && node.children.length > 0) {
      node.children.forEach((child, idx) => {
        collectIds(child, `${id}-${idx}`)
      })
    }
    if (node.decoded_header) {
      collectIds(node.decoded_header, `${id}-decoded-header`)
    }
    if (node.decoded_payload) {
      collectIds(node.decoded_payload, `${id}-decoded-payload`)
    }
  }
  collectIds(props.tree)
  expandedNodes.value = allIds
}

const collapseAll = () => {
  expandedNodes.value = new Set()
}
</script>

<template>
  <div class="derivation-tree-container">
    <div class="tree-header">
      <h3> Árbol de Derivaciones</h3>
      <div class="tree-controls">
        <button @click="expandAll" class="btn-tree">Expandir Todo</button>
        <button @click="collapseAll" class="btn-tree">Colapsar Todo</button>
      </div>
    </div>

    <div class="tree-content">
      <TreeNode 
        :node="tree" 
        :path="'root'"
        :expandedNodes="expandedNodes"
        @toggle="toggleNode"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'DerivationTree',
  components: {
    TreeNode: {
      name: 'TreeNode',
      props: {
        node: Object,
        path: String,
        expandedNodes: Set
      },
      template: `
        <div class="tree-node">
          <div class="node-content" @click="$emit('toggle', path)">
            <span class="node-icon" v-if="hasChildren">
              {{ isExpanded ? '▼' : '▶' }}
            </span>
            <span class="node-icon-leaf" v-else>●</span>
            
            <span class="node-type">{{ node.type }}</span>
            
            <span class="node-rule" v-if="node.rule">{{ node.rule }}</span>
            
            <span class="node-value" v-if="node.value">
              <code>{{ node.value }}</code>
            </span>
            
            <span class="node-chars" v-if="node.characters">
              <span class="char-badge" v-for="(char, idx) in node.characters" :key="idx">
                {{ char }}
              </span>
            </span>
          </div>

          <div v-if="isExpanded && hasChildren" class="node-children">
            <TreeNode 
              v-for="(child, idx) in node.children"
              :key="idx"
              :node="child"
              :path="path + '-' + idx"
              :expandedNodes="expandedNodes"
              @toggle="(id) => $emit('toggle', id)"
            />
            
            <div v-if="node.decoded_header" class="decoded-section">
              <div class="section-label">Header Decodificado:</div>
              <TreeNode 
                :node="node.decoded_header"
                :path="path + '-decoded-header'"
                :expandedNodes="expandedNodes"
                @toggle="(id) => $emit('toggle', id)"
              />
            </div>
            
            <div v-if="node.decoded_payload" class="decoded-section">
              <div class="section-label">Payload Decodificado:</div>
              <TreeNode 
                :node="node.decoded_payload"
                :path="path + '-decoded-payload'"
                :expandedNodes="expandedNodes"
                @toggle="(id) => $emit('toggle', id)"
              />
            </div>
          </div>
        </div>
      `,
      computed: {
        hasChildren() {
          return (this.node.children && this.node.children.length > 0) || 
                 this.node.decoded_header || 
                 this.node.decoded_payload
        },
        isExpanded() {
          return this.expandedNodes.has(this.path)
        }
      }
    }
  }
}
</script>

<style scoped>
.derivation-tree-container {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
}

.tree-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
}

.tree-header h3 {
  color: #667eea;
  margin: 0;
  font-size: 1.3rem;
}

.tree-controls {
  display: flex;
  gap: 10px;
}

.btn-tree {
  padding: 8px 16px;
  background: white;
  border: 2px solid #667eea;
  color: #667eea;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.btn-tree:hover {
  background: #667eea;
  color: white;
}

.tree-content {
  background: white;
  border-radius: 8px;
  padding: 15px;
  max-height: 600px;
  overflow-y: auto;
}

.tree-node {
  margin-left: 20px;
  border-left: 2px solid #e0e0e0;
  padding-left: 15px;
  margin-bottom: 5px;
}

.node-content {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
  flex-wrap: wrap;
}

.node-content:hover {
  background: #f0f0f0;
}

.node-icon {
  color: #667eea;
  font-weight: bold;
  width: 16px;
  text-align: center;
}

.node-icon-leaf {
  color: #999;
  font-size: 0.6rem;
  width: 16px;
  text-align: center;
}

.node-type {
  font-weight: 600;
  color: #333;
  background: #e3f2fd;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.node-rule {
  color: #666;
  font-style: italic;
  font-size: 0.85rem;
  background: #fff3cd;
  padding: 4px 8px;
  border-radius: 4px;
}

.node-value {
  color: #28a745;
  font-family: 'Courier New', monospace;
}

.node-value code {
  background: #e8f5e9;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.node-chars {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.char-badge {
  background: #667eea;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  font-weight: 600;
}

.node-children {
  margin-top: 5px;
}

.decoded-section {
  margin-top: 15px;
  padding-top: 10px;
  border-top: 1px dashed #ccc;
}

.section-label {
  font-weight: 600;
  color: #764ba2;
  margin-bottom: 10px;
  padding-left: 5px;
}

/* Scrollbar personalizado */
.tree-content::-webkit-scrollbar {
  width: 8px;
}

.tree-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.tree-content::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 4px;
}

.tree-content::-webkit-scrollbar-thumb:hover {
  background: #5568d3;
}
</style>
