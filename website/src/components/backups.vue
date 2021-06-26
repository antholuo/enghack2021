<template>
    <div class="md-layout">
                        <v-card class="px-8" tile flat>
                                    <v-list-item>
                                        <v-list-item-content>
                                        <v-list-item-title class="text-h6">
                                            List of Backups
                                        </v-list-item-title>
                                        <v-list-item-subtitle>
                                            this should now be running on it's own
                                        </v-list-item-subtitle>
                                        </v-list-item-content>
                                    </v-list-item>

                                    <v-divider></v-divider>

                                    <v-list
                                        dense
                                        nav
                                    >
                                        <v-list-item
                                        v-for="item in items"
                                        :key="item.title"
                                        link
                                        >
                                        <v-list-item-icon>
                                            <v-icon>{{ item.icon }}</v-icon>
                                        </v-list-item-icon>

                                        <v-list-item-content>
                                            <v-row>
                                                <v-col>
                                                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                                                </v-col>
                                                <v-col align="end">
                                                    <v-btn
                                                    :loading="loading3"
                                                    :disabled="loading3"
                                                    color="blue-grey"
                                                    class="ma-2 white--text"
                                                    @click="loader = 'loading2'"
                                                    >
                                                    Image
                                                    <v-icon
                                                        right
                                                        light
                                                    >
                                                        mdi-download
                                                    </v-icon>
                                                    </v-btn>
                                                </v-col>
                                            </v-row>
                                        </v-list-item-content>
                                        </v-list-item>
                                    </v-list>
                        </v-card>
    </div>
</template>

<script>
export default {
    name: 'backups',
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
          { title: 'Dashboard', icon: 'mdi-view-dashboard' },
          { title: 'Photos', icon: 'mdi-image' },
          { title: 'About', icon: 'mdi-help-box' },
        ],
    })
}