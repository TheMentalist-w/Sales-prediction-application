<template>
  <v-dialog v-model="dialogDelete" max-width="500px">
    <v-card>
      <v-card-title class="text-h5">Are you sure you want to delete this item?</v-card-title>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="red darken-1" rounded text @click="closeDelete">Cancel</v-btn>
        <v-btn color="green darken-1" rounded text @click="deleteItemConfirm">OK</v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from "axios";

export default {
  name: "DialogDelete",
  props: {
    dialogDelete: Boolean,
    deleteId: Number,
    editedIndex: Number,
    username: String,
  },
  methods: {
    deleteItemConfirm () {
      let username = this.username
      let index = this.editedIndex
      axios.get('http://localhost:8000/pitbull/user/current/')
        .then((response) => {
          if(response.data.username === username) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Cannot delete yourself',
              type: 'error text-white'
            })
          } else {
            axios.delete('http://localhost:8000/pitbull/user/delete/'+this.deleteId.toString())
              .then(() => {
                this.$emit('deleteFromArray', index)
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Success',
                  text: 'User deleted',
                  type: 'success text-white'
                })
              })
              .catch(() => this.$notify({
                group: 'notifications-bottom-left',
                title: 'Error',
                text: 'Error deleting user',
                type: 'error text-white'
              }))
          }
        })
      this.closeDelete()
    },
    closeDelete() {
      this.$emit('closeDelete')
    }
  },
}
</script>

<style scoped>

</style>
