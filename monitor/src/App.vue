<template>
  <v-app>
    <v-app-bar
      app
      color="orange darken-4"
      dark
    >
      <div class="d-flex align-center">
        <h1>COURIER - Topics Monitor</h1>
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/Grubbly/Courier"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-content class="grey darken-3">
      <Log />
    </v-content>
  </v-app>
</template>

<script>
import Log from '@/components/Log'

export default {
  name: 'App',

  components: {
    Log,
  },

  data: () => ({
    //
  }),
};
</script>
