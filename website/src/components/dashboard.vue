<template>
    <div class="md-layout">
        <v-container>
            <v-card class="my-8 mx-auto"
            elevation=2
            shaped>
                <v-card-actions>
                    <v-row align="center"
                    justify="end">
                    <v-btn
                        color="orange"
                        text>
                        Share
                    </v-btn>
                    </v-row>
                </v-card-actions>
                <v-row align="center"
                justify="start">
                <v-card-title>This is the dashboard!</v-card-title>
                <v-card-subtitle>Here you'll find all the information about the last backups at a glance</v-card-subtitle>
                </v-row>


                <v-container
                    class="grey lighten-5 mb-6"
                    >
                    <v-row
                        align="center"
                    >
                        <v-col>
                            <v-progress-circular
                                :value="100"
                                color="blue-grey"
                                size="70"
                                width="35"
                            ></v-progress-circular>
                        </v-col>
                        <v-col>
                            Should contain brief overview
                        </v-col>
                        <v-col>
                            Should contain a button to image OS
                        </v-col>
                    </v-row>
                </v-container>


            </v-card>
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
    })
}
</script>

<style lang="scss" scoped>

  .md-layout-item {
    height: 80px;
  }
</style>