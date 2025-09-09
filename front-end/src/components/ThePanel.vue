<template>
    <div class="panel container">
            <h2>{{ itemType }}s</h2>
            <TheTable>
                <template #table-header>
                    <tr>
                        <th>Name</th>
                        <th>Relations</th>
                    </tr>
                </template>
                <template #table-body>
                    <tr v-for="item in items">
                        <td>{{ item.node.replace(itemType.toLowerCase()+"_", '') }}</td>
                        <td>{{ item.relationships }}</td>
                    </tr>
                </template>
            </TheTable>
    </div>
</template>

<script setup>
import TheTable from './TheTable.vue';
const props = defineProps({
    items: {
        type: Array,
        required: true,
    },
    itemType: {
        type: String,
        required: true,
    },
});
</script>