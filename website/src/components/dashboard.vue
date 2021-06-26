<template>
    <div class="md-layout">
        <v-container>
            <v-row justify="space-around">
            <v-card class="dash_card"
            elevation=2
            shaped
            width="600">
                <v-card-title>This is the dashboard!</v-card-title>
                <v-card-text>Here you'll find all the information about the last backups at a glance</v-card-text>
            </v-card>
            </v-row>
        </v-container>
    </div>
</template>

<script>
export default {
    name: 'dashboard',
    setup() {
        
    },
    data: () => ({

    })
}
</script>

<style lang="scss" scoped>

  .md-layout-item {
    height: 80px;
  }
</style>