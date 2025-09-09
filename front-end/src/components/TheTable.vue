<template>
    <table class="table table-hover xtable">
        <thead class="table-danger">
            <slot name="table-header">
                <tr>
                    <th>Name</th>
                    <th>Relations</th>
                </tr>
            </slot>
        </thead>
        <tbody>
            <slot name="table-body">
                <tr>
                    <td>Name</td>
                    <td>Relations</td>
                </tr>
            </slot>
        </tbody>
    </table>
</template>

<style scoped>
@media (min-width: 1024px) {}
.xtable {
    text-align: center;
    line-height: 25px;
    table-layout: fixed; width: 100%
    
}

</style>

<script setup>
</script>