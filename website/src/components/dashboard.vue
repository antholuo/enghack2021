<template>
    <div class="md-layout">
        <v-container>
            <v-img
                :src="require('../assets/logo.svg')"
                class="my-3"
                contain
                height="200"
                />
            <v-row>
            <v-col></v-col>
            <v-col md="8">
            <v-card class="my-8 mx-12"
            elevation=2
            shaped>

                <v-container
                    class="grey lighten-5 mb-6"
                    >
                    <v-row
                        align="center"
                    >
                        <v-col
                        align="center">
                            <v-progress-circular
                                :value="100"
                                color="blue-grey"
                                size="70"
                                width="35"
                            ></v-progress-circular>
                        </v-col>
                        <v-col
                        align="center"
                        md="6">
                            <v-card-title>Status: Backed Up</v-card-title>
                        </v-col>
                        <v-col align="center">
                            <v-card-actions>
                                <v-btn
                                :loading="loading3"
                                :disabled="loading3"
                                color="blue-grey"
                                class="ma-2 white--text"
                                @click="loader = 'loading3'"
                                >
                                Backup
                                <v-icon
                                    right
                                    dark
                                >
                                    mdi-cloud-upload
                                </v-icon>
                                </v-btn>
                            </v-card-actions>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card>
            <v-row class="py-2" justify="center">
                THERE CAN BE MORE TEXT HERE
            </v-row>
            </v-col>
            <v-col></v-col>
            </v-row>
        </v-container>
        <v-row>
            <v-col md="12">    
                <v-row no-gutters>
                    <v-col md="2"></v-col>
                    <v-col md="3">
                        <v-card dark tile flat color="error">Stats here</v-card>
                    </v-col>
                    <v-col md="5">
                        <v-card dark tile flat color="pink darken-4">List of backups here</v-card>
                    </v-col>
                    <v-col md="2"></v-col>
                </v-row>
            </v-col>
        </v-row>
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
    })
}
</script>

<style lang="scss" scoped>

  .md-layout-item {
    height: 80px;
  }
</style>