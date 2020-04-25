<template>
  <v-container fluid class="grey lighten-3">
      <v-row>
          <v-col
            v-for="item in items"
            :key="item.topic"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card>
              <v-card-title class="white--text indigo subheading font-weight-bold">
                {{ item.topic }} 
              </v-card-title>
              <v-col align="center">
                Most Recent Payload:
                <v-chip dark class="ma-2" color="blue darken-4">
                 {{item.current}}
                </v-chip>
              </v-col>
              <v-divider></v-divider>
              <v-list>
                <v-list-item>
                    <v-list-item-content class="align-end">
                        <v-data-table
                            :headers="headers"
                            :items="item.payloads"
                            :items-per-page="5"
                            class="elevation-1"
                        ></v-data-table>
                    </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
  </v-container>
</template>

<script>
import LogData from '@/data/mqtt_data.json'

export default {
    name: 'LogTable',
    data() {
        return {
            headers: [
                {
                    text: 'Timestamp',
                    align: 'start',
                    value: 'timestamp'
                },
                {
                    text: 'Payload',
                    value: 'payload'
                }
            ],
            items: []
        }
    },
    created() {
        var topics = LogData['topics']
        topics.forEach(topic => {
            console.log(topic)
            this.items.push(
                {
                    "topic": topic,
                    "payloads": LogData["history"][topic],
                    "current": LogData["current"][topic]
                }
            )
        });
    }
}
</script>

<style>

</style>