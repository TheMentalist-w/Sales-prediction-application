<template>
  <v-dialog
    v-model="dialogDelete"
    max-width="535px"
  >
    <v-card>
      <v-card-title class="text-h5">
        Are you sure you want to delete this account?
      </v-card-title>
      <v-card-actions>
        <v-spacer />
        <v-btn
          color="red darken-1"
          rounded
          text
          @click="closeDelete"
        >
          Cancel
        </v-btn>
        <v-btn
          color="green darken-1"
          rounded
          text
          @click="deleteItemConfirm"
        >
          OK
        </v-btn>
        <v-spacer />
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DialogDelete',
  props: {
    dialogDelete: Boolean,
    // eslint-disable-next-line vue/require-default-prop
    deleteId: Number,
    // eslint-disable-next-line vue/require-default-prop
    editedIndex: Number,
    // eslint-disable-next-line vue/require-default-prop
    username: String
  },
  methods: {
    deleteItemConfirm () {
      const index = this.editedIndex;
      axios.delete('/user_authorization/delete/' + this.deleteId.toString() + '/')
        .then(() => {
          this.$emit('deleteFromArray', index);
          this.$notify({
            group: 'notifications-bottom-left',
            title: 'Success',
            text: 'User deleted',
            type: 'success text-white'
          });
        })
        .catch((error) => {
          if (error.response.status === 409) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: error.response.data,
              type: 'error text-white'
            });
          } else if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error.Try later',
              type: 'error text-white'
            });
          } else {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Error deleting user',
              type: 'error text-white'
            });
          }
        });
      this.closeDelete();
    },

    closeDelete () {
      this.$emit('closeDelete');
    }
  }
};
</script>

<style scoped>

</style>
