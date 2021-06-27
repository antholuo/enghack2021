<template>
    <v-app>
        <v-app-bar
            app
            color="secondary"
            dark
        >
            <div class="d-flex align-center">
                <v-img
                    alt="Vuetify Logo"
                    class="shrink mr-2"
                    contain
                    src="https://www.pinclipart.com/picdir/big/364-3648446_poggers-emote-clipart.png"
                    transition="scale-transition"
                    width="40"
                />
                <h1>PogOS</h1>
            </div>

            <v-spacer></v-spacer>

            <v-btn
                href="https://github.com/antholuo/enghack2021"
                target="_blank"
                text
            >
                <span class="mr-2">Github</span>
                <v-icon>mdi-open-in-new</v-icon>
            </v-btn>
        </v-app-bar>

        <v-main>
            <v-row>
                <v-col>
                    <v-card class="my-8 mx-12"
                            elevation=2
                            shaped>
                        <v-card-title>Git Remote</v-card-title>
                        <v-card-text>
                            <v-text-field prepend-icon="mdi-web" label="HTTPS URL"></v-text-field>
                            <v-text-field prepend-icon="mdi-account" label="User Name"></v-text-field>
                            <v-text-field prepend-icon="mdi-lock" :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                                          label="Password" :type="show?'text':'password'" @click:append="show = !show"
                            ></v-text-field>
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-card class="mx-12"
                            elevation=2
                    >
                        <v-card-text>
                            <v-list>
                                <v-list-item-group>
                                    <v-list-item v-for="(step, i) of this.steps" :key="step">
                                            <v-list-item-action>
                                                <v-checkbox v-if="currentStep>i" :input-value="true"></v-checkbox>
                                                <v-checkbox v-else-if="currentStep<i"  :input-value="false"></v-checkbox>
                                                <v-progress-circular size="20" v-else indeterminate></v-progress-circular>
                                            </v-list-item-action>
                                            <v-list-item-content>
                                                <v-list-item-title>{{step}}</v-list-item-title>
                                            </v-list-item-content>
                                    </v-list-item>
                                </v-list-item-group>
                            </v-list>
                        </v-card-text>
                        <v-card-actions>
                            <v-row>
                                <v-col>
                                    <v-btn
                                        block
                                        x-large
                                        :loading="backingUp"
                                        :disabled="backingUp"
                                        color="info"
                                        @click="backingUp = 'true'"
                                    >
                                        <v-icon left>mdi-cloud-upload</v-icon>
                                        Backup
                                        <template v-slot:loader>
                                    <span class="custom-loader">
                                      <v-icon light>mdi-cached</v-icon>
                                    </span>
                                        </template>
                                    </v-btn>
                                </v-col>
                                <v-col>
                                    <v-btn
                                        block
                                        x-large
                                        :loading="restoring"
                                        :disabled="restoring"
                                        color="success"
                                        @click="restoring = 'true'"
                                    >
                                        <v-icon left>mdi-cloud-download</v-icon>
                                        Restore
                                        <template v-slot:loader>
                                    <span class="custom-loader">
                                      <v-icon light>mdi-cached</v-icon>
                                    </span>
                                        </template>
                                    </v-btn>
                                </v-col>
                            </v-row>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-main>
    </v-app>
</template>

<script>

export default {
    name: 'App',

    components: {},
    computed: {
        steps() {
            return this.backingUp?this.backupSteps:this.restoreSteps
        },
    },
    data: () => ({
        show: false,
        backingUp: false,
        restoring: false,
        backupSteps:[
            'Initializing git repo',
            'Listing applications',
            'Archiving app data',
            'Pushing to git remote'
        ],
        restoreSteps:[
            'Fetching backup',
            'Installing applications',
            'Restoring application data'
        ],
        currentStep:1
    }),
};
</script>
<style scoped>
.custom-loader {
    animation: loader 1s infinite;
    display: flex;
}

@-moz-keyframes loader {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}

@-webkit-keyframes loader {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}

@-o-keyframes loader {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}

@keyframes loader {
    from {
        transform: rotate(0);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>
