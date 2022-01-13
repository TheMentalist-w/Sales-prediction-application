<template>
  <v-card>
    <v-card-title>
      <span class="text-h5">{{ formTitle }}</span>
    </v-card-title>
    <v-card-text>
      <v-container>
        <v-row>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-model="editedItem.first_name"
              label="Name"
            />
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-model="editedItem.last_name"
              label="Surname"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-model="editedItem.email"
              class="emailField"
              type="email"
              label="Email"
              :rules="[rules.email]"
            />
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-model="editedItem.username"
              class="usernameField"
              :items="type"
              label="Username"
            />
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-select
              v-model="editedItem.type"
              :items="type"
              label="Type"
            />
          </v-col>
          <v-col
            cols="12"
            md="12"
          >
            <v-checkbox
              v-if="isEdited"
              v-model="checkbox"
              label="Reset password"
              color="primary"
              hide-details
            />
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-if="showPasswordModal"
              v-model="editedItem.password"
              class="passwordField"
              type="password"
              :rules="[rules.newUser]"
              label="Password"
            />
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-if="showPasswordModal"
              v-model="editedItem.confirmPassword"
              type="password"
              :rules="[rules.password]"
              label="Confirm password"
            />
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn
        color="red darken-1"
        text
        rounded
        @click="close"
      >
        Cancel
      </v-btn>
      <v-btn
        color="green darken-1"
        text
        rounded
        @click="save"
      >
        Save
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EmployeeModal',
  props: {
    // eslint-disable-next-line vue/require-default-prop
    formTitle: String,
    // eslint-disable-next-line vue/require-default-prop
    editedItem: Object,
    // eslint-disable-next-line vue/require-default-prop
    editedIndex: Number
  },
  data () {
    return {
      checkbox: false,
      type: ['Normal', 'Admin'],
      rules: {
        password: () => {
          const result = this.editedItem.password === this.editedItem.confirmPassword;
          return result || "Password and Confirm Password don't match";
        },
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
          return pattern.test(value) || 'Invalid e-mail';
        },
        newUser: value => {
          const result = (value === null || value === '');
          return !((this.editedIndex < 0 && result) || (this.checkbox && result)) || 'Password required';
        }
      }
    };
  },
  computed: {
    showPasswordModal () {
      return (!this.isEdited || this.checkbox);
    },
    isEdited () {
      return this.editedIndex !== -1;
    }
  },
  methods: {
    createForm () {
      const data = new FormData();
      data.append('first_name', this.editedItem.first_name);
      data.append('email', this.editedItem.email);
      data.append('last_name', this.editedItem.last_name);
      data.append('username', this.editedItem.username);
      data.append('password', this.editedItem.password ? this.editedItem.password : '');
      data.append('confirmPassword', this.editedItem.confirmPassword ? this.editedItem.password : '');
      return data;
    },

    validateModal () {
      let result;
      if (this.editedIndex > -1) {
        // edit
        const validate = Object.values(this.editedItem).every(field => {
          if (field === 'Normal' || field === 'Admin') {
            return true;
          } else {
            return (field === null || field === '');
          }
        });
        result = validate ? { result: false, errorMsg: 'All fields are empty' }
          : ((this.editedItem.password !== this.editedItem.confirmPassword) ? { result: false, errorMsg: 'Password and Confirm Password are different' }
            : { result: true, errorMsg: '' });
        if (this.rules.email(this.editedItem.email) !== true) {
          result = { result: false, errorMsg: 'Invalid email' };
        }
        if (this.editedItem.password === '' && this.checkbox) {
          result = { result: false, errorMsg: 'Password required' };
        }
      } else {
        // create
        const validate = Object.values(this.editedItem).every(field => (field === null || field === ''));
        const validateAny = Object.values(this.editedItem).some(field => field === '');
        result = validate ? { result: false, errorMsg: 'All fields are empty' }
          : (validateAny ? { result: false, errorMsg: 'Some fields are empty' }
            : ((this.editedItem.password !== this.editedItem.confirmPassword) ? { result: false, errorMsg: 'Password and Confirm Password are different' }
              : { result: true, errorMsg: '' }));
        if (this.rules.email(this.editedItem.email) !== true) {
          result = { result: false, errorMsg: 'Invalid email' };
        }
      }
      return result;
    },

    save () {
      const validate = this.validateModal();
      if (validate.result) {
        const data = this.createForm();
        if (this.editedIndex > -1) {
          data.append('id', this.editedItem.id);
          data.append('is_superuser', this.editedItem.type === 'Admin');
          axios.patch('/user_authorization/edit/', data)
            .then(() => {
              this.$emit('editEmployee', this.editedItem);
              this.$notify({
                group: 'notifications-bottom-left',
                title: 'Success',
                text: 'Employee edited',
                type: 'success text-white'
              });
              this.close();
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
                  text: 'Employee edit error',
                  type: 'error text-white'
                });
                this.close();
              }
            });
        } else {
          if (this.editedItem.type === 'Admin') {
            axios.post('/user_authorization/superuser/create/', data)
              .then((response) => {
                this.editedItem.id = response.data.new_user_id;
                this.addEmployee();
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Success',
                  text: 'Employee added',
                  type: 'success text-white'
                });
                this.close();
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
                    text: 'Employee addition error',
                    type: 'error text-white'
                  });
                  this.close();
                }
              });
          } else {
            axios.post('/user_authorization/create/', data)
              .then((response) => {
                this.editedItem.id = response.data.new_user_id;
                this.addEmployee();
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Success',
                  text: 'Employee added',
                  type: 'success text-white'
                });
                this.close();
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
                    text: 'Employee addition error',
                    type: 'error text-white'
                  });
                  this.close();
                }
              });
          }
        }
      } else {
        this.$notify({
          group: 'notifications-bottom-left',
          title: 'Error',
          text: validate.errorMsg,
          type: 'error text-white'
        });
      }
    },

    close () {
      this.$emit('closeModal');
    },

    addEmployee () {
      this.$emit('addEmployee', this.editedItem);
    }
  }
};
</script>

<style scoped>

</style>
