<template>
    <div class="tile mt-2">
        <div class="row">
            <div class="col">
                <h2>{{ itemType }}s</h2>
            </div>
            <div class="col">
            </div>
        </div>
        <div class="row row-cols-1 row-cols-md-4 g-1">
            <div v-for="item in items" :key="item.node" class="col">
                <div class="card border-danger mb-3" style="max-width: 18rem;">
                    <div class="card-header xheader"><b>{{ item.node.replace(itemType.toLowerCase()+"_", '') }}</b></div>
                    <div class="card-body">
                        <p v-for="relation in item.relationships" :key="relation" class="card-text">{{ relation }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

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

<style scoped>
.card-header {
    background-color: #FF3621;
    color: white;
}
.card-body {
    background-color: #FFF;
    color: black;
    font-size: small;
}
</style>