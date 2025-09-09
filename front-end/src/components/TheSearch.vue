<template>
  <div class="search mt-2">
  <TheSpinner :isLoading="isLoading">
    <template #content>
      <h4>Select an Entity</h4>
      <form class="d-flex">
        <input class="form-control" type="search" v-model="input" placeholder="Type to search entities..." @input="formChange()"/>
      </form>
      <div class="results" v-if="results">
        <div class="result-item" v-for="item in filteredList()" :key="item" @click="selectItem(item)">
          {{ item }}
        </div>
      <div v-if="input && !filteredList().length">
        <p>No results found!</p>
      </div>
      </div>
    </template>
  </TheSpinner>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { get_entities } from "../services/apiService";
import { toast } from "vue3-toastify";
import TheSpinner from "@/components/TheSpinner.vue";

const isLoading = ref(false);
const data = ref({});
const input = ref("");
const entity = defineModel();
const results = ref(false);

onMounted(() => {
  fetchData();
});

async function fetchData() {
  try {
    isLoading.value = true;
    data.value = await get_entities(entity.value); // Ensure entity.value is used
  } catch (error) {
    toast("Error fetching table data: " + error.message);
    console.error("Error fetching graph data:", error);
  } finally {
    isLoading.value = false;
  }
}

function formChange() {
  results.value = true;
}

function filteredList() {
  results.value = true; // Indicate that filtering is in progress
  try {
    if (!input.value.trim()) {
      return [];
    }
    // Filter the data based on input value and specific conditions
    return data.value
      .filter(item => 
        Object.values(item).some(val =>
          String(val).toLowerCase().includes(input.value.toLowerCase())
        )
      )
      .filter(item => item.attributes.label === "entity") // Filter by 'entity' attribute
      .map(item => item.node); // Map the filtered items to their 'node' property
  } catch (error) {
    toast("Error filtering data: " + error.message);
    console.error("Error filtering list:", error);
    return [];
  }
}



function selectItem(item) {
  input.value = item;
  entity.value = item;
  results.value = false; // Hide results after selection
  // Additional logic (e.g., navigation) can be added here
}


</script>

<style scoped>
.results {
  position: absolute;
  background-color: white;
  border: 1px solid #ccc;
  z-index: 1000;
  width: 100%;
}
.result-item {
  padding: 10px;
  cursor: pointer;
}
</style>