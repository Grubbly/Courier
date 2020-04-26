<template>
  <v-container>
      <v-row class="text-center">
          <v-col>
              <v-card>
                  <LogTable />
              </v-card>
          </v-col>
      </v-row>
  </v-container>
</template>

<script>
import LogTable from '@/components/LogTable'

export default {
    name: "Log",
    components: {
        LogTable
    }
}
</script>

<style>

</style>