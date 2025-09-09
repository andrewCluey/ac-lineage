<template>
  <main>
    <div class="container">
    <TheSearch v-model="entity"></TheSearch>
    <div v-show="entity.length > 0" class="row mt-2">
            <div class="col">
                <h2>{{entity}}</h2>
            </div>
             <div class="col">
            <button type="button" class="btn btn-danger" @click="refreshCache()" :disabled="isRefreshing">
                    <span v-if="isRefreshing" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
                    {{ isRefreshing ? 'Refreshing...' : 'Refresh Cache' }}
            </button>
        </div>
    </div>
    <div v-show="entity.length > 0" class="row">
        <div class="col">
                <div class="btn-group me-3" role="group" aria-label="View toggle">
                    <input type="radio" class="btn-check" name="btnradio" id="tileName" value="tiles" autocomplete="off" checked v-model="selectedModel">
                    <label class="btn btn-outline-danger" for="tileName" >Tiles</label>
                    <input type="radio" class="btn-check" name="btnradio" id="tableName" value="table" autocomplete="off" v-model="selectedModel">
                    <label class="btn btn-outline-danger" for="tableName">Table</label>
                </div>
            </div>
            <div class="col">
                <div class="btn-group me-3" role="group" aria-label="Account Users toggle">
                    <input type="radio" class="btn-check" name="accountUsers" id="accountUsersOff" :value="false" autocomplete="off" v-model="accountUsersEnabled">
                    <label class="btn btn-outline-secondary" for="accountUsersOff">Account Users Off</label>
                    <input type="radio" class="btn-check" name="accountUsers" id="accountUsersOn" :value="true" autocomplete="off" v-model="accountUsersEnabled">
                    <label class="btn btn-outline-secondary" for="accountUsersOn">Account Users On</label>
                </div>
            </div>
    </div>
    <TheGraph :entity="entity" :account-users-enabled="accountUsersEnabled"></TheGraph>
    <div v-show="selectedModel !== 'table'" class="row mt-2">
    <TheTiles v-if="data.membership.length > 0" :items="data.membership" item-type="Membership"></TheTiles>
    <TheTiles v-if="data.catalogs.length > 0" :items="data.catalogs" item-type="Catalog"></TheTiles>
    <TheTiles v-if="data.schemas.length > 0" :items="data.schemas" item-type="Schema"></TheTiles>
    <TheTiles v-if="data.warehouses.length > 0" :items="data.warehouses" item-type="Warehouse"></TheTiles>
    <TheTiles v-if="data.clusters.length > 0" :items="data.clusters" item-type="Cluster"></TheTiles>
    </div>
    <div v-show="selectedModel === 'table'" class="row mt-2">
    <ThePanel v-if="data.membership.length > 0" :items="data.membership" item-type="Membership"></ThePanel>
    <ThePanel v-if="data.catalogs.length > 0" :items="data.catalogs" item-type="Catalog"></ThePanel>
    <ThePanel v-if="data.schemas.length > 0" :items="data.schemas" item-type="Schema"></ThePanel>
    <ThePanel v-if="data.warehouses.length > 0" :items="data.warehouses" item-type="Warehouse"></ThePanel>
    <ThePanel v-if="data.clusters.length > 0" :items="data.clusters" item-type="Cluster"></ThePanel>
    </div>
    </div>




  </main>
</template>

<script setup>
import TheGraph from '@/components/TheGraph.vue';
import TheSearch from '@/components/TheSearch.vue';
import ThePanel from '@/components/ThePanel.vue';
import TheTiles from '@/components/TheTiles.vue';
import { get_entity_relations, get_entity_relations_filtered, refresh_cache, get_entities } from '@/services/apiService';
import { watch } from 'vue';
import { ref } from 'vue';
import { toast } from 'vue3-toastify';

const selectedModel = ref("tiles")
const entity = ref("");
const isLoading = ref(false);
const isRefreshing = ref(false);
const accountUsersEnabled = ref(false);
const data = ref({
    membership: [],
    catalogs: [],
    schemas: [],
    tables: [],
    warehouses: [],
    clusters: [], 
});

watch(() => entity.value, (newValue) => {
    fetchData(newValue);
});

watch(() => accountUsersEnabled.value, (newValue) => {
    if (entity.value) {
        fetchData(entity.value);
    }
});

async function fetchData(entityItem) {
    if (!entityItem || entityItem === "") {
        return;
    }
    try {
        isLoading.value = true;
        data.value = {
            membership: [],
            catalogs: [],
            schemas: [],
            tables: [],
            warehouses: [],
            clusters: [], };
        var results = accountUsersEnabled.value 
            ? await get_entity_relations(entityItem)
            : await get_entity_relations_filtered(entityItem);
        results.map(item => {
            if (item.label === "entity") {
                data.value.membership.push(item);
            } else if (item.label === "catalog") {
                data.value.catalogs.push(item);
            } else if (item.label === "schema") {
                data.value.schemas.push(item);
            } else if (item.label === "table") {
                data.value.tables.push(item);
            } else if (item.label === "warehouse") {
                data.value.warehouses.push(item);
            } else if (item.label === "cluster") {
                data.value.clusters.push(item);
            }
        });
    } catch (error) {
        toast("Error fetching graph data :" + error);
        console.error("Error fetching graph data:", error);
    } finally {
        isLoading.value = false;
    }
}

async function refreshCache() {
    try {
        isRefreshing.value = true;
        await refresh_cache();
        toast("Cache refreshed successfully!", {
            type: "success"
        });
        // Refresh current entity data if one is selected
        if (entity.value) {
            await fetchData(entity.value);
        }
    } catch (error) {
        toast("Error refreshing cache: " + error.message, {
            type: "error"
        });
        console.error("Error refreshing cache:", error);
    } finally {
        isRefreshing.value = false;
    }
}
</script>

<style lang="sass">

</style>