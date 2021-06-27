<template>
    <div class="md-layout">
        <v-container>
            <v-card class="my-8 mx-12"
                    elevation=2
                    shaped>
                <v-container
                    class="grey lighten-5 mb-6"
                >
                    <v-card-title>Git Remote</v-card-title>
                   <v-card-text>
                       <v-text-field label="HTTPS URL"></v-text-field>
                       <v-text-field label="User Name"></v-text-field>
                       <v-text-field label="Password" type="password"></v-text-field>
                   </v-card-text>
                </v-container>
            </v-card>
            <v-row class="py-2" justify="center">
                THERE CAN BE MORE TEXT HERE
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
        alignments: [
            'start',
            'center',
            'end',
        ],
        selectedItem: 1,
        items: [
            {title: 'Dashboard', icon: 'mdi-view-dashboard'},
            {title: 'Photos', icon: 'mdi-image'},
            {title: 'About', icon: 'mdi-help-box'},
        ],
    }),
};
</script>

<style lang="scss" scoped>

.md-layout-item {
    height: 80px;
}
</style>