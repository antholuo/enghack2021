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
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />
        <h1>Brought to you by the fledglings</h1>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Go to the github</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <dashboard/>
      <v-row>
            <v-col md="12">    
                <v-row no-gutters>
                    <v-col md="2"></v-col>
                    <v-col md="3">
                        <v-card tile flat color="error">Stats here</v-card>
                    </v-col>
                    <v-col md="5">
                        <backups/>
                    </v-col>
                    <v-col md="2"></v-col>
                </v-row>
            </v-col>
        </v-row>
      <HelloWorld/>
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';
import dashboard from './components/dashboard';
import backups from './components/backups';

export default {
  name: 'App',

  components: {
    HelloWorld,
    dashboard,
    backups,
  },

  data: () => ({
    //
  }),
};
</script>
