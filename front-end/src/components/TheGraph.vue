<template>
  <div v-show="entity.length > 0" class="graph mt-2">
    <div class="row">
      <div class="col">
        <h2>Graph</h2>
      </div>
    </div>
  </div>
  <div v-show="!isLoading" id="mynetwork" ref="visContainerElement"></div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue';
import { Network } from 'vis-network';
import { get_entity } from '../services/apiService';
import { toast } from 'vue3-toastify';

import root from '@/assets/root.svg';
import schema from '@/assets/schema.svg';
import warehouse from '@/assets/warehouse.svg';
import group from '@/assets/entity.svg';
import catalog from '@/assets/catalog.svg';
import cluster from '@/assets/cluster.svg';

const props = defineProps({
  entity: {
    type: String,
    required: true,
  },
  accountUsersEnabled: {
    type: Boolean,
    default: false,
  },
});

const nodes = ref([]);
const edges = ref([]);
const isLoading = ref(false);
const visContainerElement = ref(null);
const options = reactive({
  interaction: { hover: true },
  physics: {
    forceAtlas2Based: { springLength: 100 },
    minVelocity: 0.75,
    solver: "forceAtlas2Based",
  },
  layout: {},
});

let networkInstance = null;

const imageMap = {
  root,
  schema,
  warehouse,
  entity: group,
  catalog,
  cluster,
};

watch(() => props.entity, fetchData);

// Watch accountUsersEnabled prop to filter nodes and edges
watch(() => props.accountUsersEnabled, (enabled) => {
  if (!enabled) {
    const accountUsersEdges = edges.value.filter(edge => edge.from === "account users");
    const targetNodeIds = accountUsersEdges.map(edge => edge.to);

    const filteredNodes = nodes.value.filter(node => !targetNodeIds.includes(node.id));
    const filteredEdges = edges.value.filter(edge => edge.from !== "account users");

    if (networkInstance) {
      networkInstance.setData({ nodes: filteredNodes, edges: filteredEdges });
    }
  } else {
    // Restore all nodes and edges by re-fetching data
    fetchData(props.entity);
  }
});

onMounted(createNetwork);

async function fetchData(entityItem) {
  isLoading.value = true;
  try {
    const response = await get_entity(entityItem);
    updateGraphData(response.nodes, response.edges);
  } catch (error) {
    handleError(error);
  } finally {
    isLoading.value = false;
  }
}

function updateGraphData(rawNodes, rawEdges) {
  nodes.value = transformNodes(rawNodes);
  edges.value = transformEdges(rawEdges);

  // Apply account users filter if needed
  let displayNodes = nodes.value;
  let displayEdges = edges.value;
  
  if (!props.accountUsersEnabled) {
    const accountUsersEdges = edges.value.filter(edge => edge.from === "account users");
    const targetNodeIds = accountUsersEdges.map(edge => edge.to);
    
    displayNodes = nodes.value.filter(node => !targetNodeIds.includes(node.id));
    displayEdges = edges.value.filter(edge => edge.from !== "account users");
  }

  if (networkInstance) {
    networkInstance.setData({ nodes: displayNodes, edges: displayEdges });
  }
}

function transformNodes(rawNodes) {
  return rawNodes.map((node) => ({
    id: node.node,
    label: node.node,
    shape: "image",
    image: imageMap[node.attributes.label] || root,
    color: "red"
  }));
}

function transformEdges(rawEdges) {
  return rawEdges.map((edge) => ({
    from: edge.source,
    to: edge.target,
  }));
}

function createNetwork() {
  if (!visContainerElement.value) return;

  networkInstance = new Network(
    visContainerElement.value,
    { nodes: nodes.value, edges: edges.value },
    options
  );
}

function handleError(error) {
  toast(`Error fetching graph data: ${error.message}`);
  console.error("Error fetching graph data:", error);
}
</script>

<style lang="css">
#mynetwork {
  width: 100%;
  height: 610px;
}
</style>