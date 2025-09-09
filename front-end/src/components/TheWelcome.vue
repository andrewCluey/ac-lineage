<script setup>
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'


</script>

<template>
  <div class="container">
  <WelcomeItem>
    <template #icon>
      <DocumentationIcon />
    </template>
    <template #heading>Databricks Permissions Viewer</template>

    Welcome to the Databricks Permissions Viewer, a powerful web application designed to simplify the visualization and management of recursive permissions in Databricks. This app provides an intuitive interface for exploring and analyzing permissions across your Databricks resources, including catalogs, schemas, tables, warehouses, and clusters.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <ToolingIcon />
    </template>
    <template #heading>Interactive Visualization</template>
    Search for any Databricks entity and explore its permissions through an interactive graph visualization. 
    View relationships between users, groups, and resources in both tile and table formats for comprehensive analysis.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <EcosystemIcon />
    </template>
    <template #heading>Permissions Analysis</template>

    Analyze recursive permissions across your Databricks ecosystem. Browse through catalogs, schemas, warehouses, 
    clusters, and their associated permissions. Understand who has access to what resources and track permission 
    inheritance through the hierarchy.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <CommunityIcon />
    </template>
    <template #heading>Getting Started</template>

    To begin exploring permissions, use the search functionality to find a specific user, group, or resource. 
    The app requires a permissions crawling workflow to populate data. Once data is available, navigate through 
    the interactive visualizations to understand your Databricks permissions landscape.
  </WelcomeItem>

  <WelcomeItem>
    <template #icon>
      <SupportIcon />
    </template>
    <template #heading>Technical Stack</template>

    Built with Vue 3 for the frontend and FastAPI for the backend, this application leverages modern web technologies 
    for optimal performance. The app integrates with Databricks APIs to fetch and visualize permissions data in 
    real-time, providing you with up-to-date insights into your access control configuration.
  </WelcomeItem>
  </div>
</template>
