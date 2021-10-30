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
              v-model="editedItem.employee"
              label="Employee"
            ></v-text-field>
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-model="editedItem.email"
              type="email"
              label="Email"
              :rules="[rules.email]"
            ></v-text-field>
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              :items="type"
              v-model="editedItem.username"
              label="Username"
            ></v-text-field>
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-select
              :items="type"
              v-model="editedItem.type"
              label="Type"
            ></v-select>
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
            ></v-checkbox>
          </v-col>
          <v-col
            cols="12"
            md="6"
          >
            <v-text-field
              v-if="showPasswordModal"
              v-model="editedItem.password"
              type="password"
              :rules="[rules.newUser]"
              label="Password"
            ></v-text-field>
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
            ></v-text-field>
          </v-col>
        </v-row>
      </v-container>
    </v-card-text>

    <v-card-actions>
      <v-spacer></v-spacer>
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
import axios from "axios";

export default {
  name: "EmployeeModal",
  data() {
    return {
      checkbox: false,
      type: ['Normal', 'Admin'],
      rules: {
        password: () => {
          let result = this.editedItem.password === this.editedItem.confirmPassword
          return result || "Password and Confirm Password don't match"
        },
        email: value => {
          let pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Invalid e-mail'
        },
        newUser: value => {
          let result = (value === null || value === '')
          return !((this.editedIndex < 0 && result) || (this.checkbox && result)) || "Password required"
        }
      },
    }
  },
  props: {
    formTitle: String,
    editedItem: Object,
    editedIndex: Number,
  },
  computed: {
    showPasswordModal () {
      return (!this.isEdited || this.checkbox)
    },
    isEdited () {
      return this.editedIndex !== -1
    },
  },
  methods: {
    createForm() {
      let data = new FormData()
      data.append("first_name", this.editedItem.employee.split(' ')[0])
      data.append("email",this.editedItem.email)
      data.append("last_name", this.editedItem.employee.split(' ')[1])
      data.append("username",this.editedItem.username)
      data.append("password", this.editedItem.password)
      data.append("confirmPassword", this.editedItem.confirmPassword)
      return data
    },

    validateModal() {
      let result
      if (this.editedIndex > -1) {
        //edit
        let validate = Object.values(this.editedItem).every(field => {
          if (field === 'Normal' || field === 'Admin') {
            return true
          } else {
            return (field === null || field === '')
          }
        })
        result = validate ? {result: false, errorMsg: "All fields are empty"} :
          ((this.editedItem.password !== this.editedItem.confirmPassword) ? {result: false, errorMsg: "Password and Confirm Password are different"} :
            {result: true, errorMsg: ""})
        if(this.rules.email(this.editedItem.email) !== true) {
          result = {result: false, errorMsg: "Invalid email"}
        }
        if(this.editedItem.password === '' && this.checkbox) {
          result = {result: false, errorMsg: "Password required"}
        }
      }
      else {
        //create
        let validate = Object.values(this.editedItem).every(field => (field === null || field === ''))
        let validateAny = Object.values(this.editedItem).some(field => field === '')
        result = validate ? {result: false, errorMsg: "All fields are empty"} :
          (validateAny ? {result: false, errorMsg: "Some fields are empty"} :
            ((this.editedItem.password !== this.editedItem.confirmPassword) ? {result: false, errorMsg: "Password and Confirm Password are different"} :
              {result: true, errorMsg: ""} ))
        if(this.rules.email(this.editedItem.email) !== true) {
          result = {result: false, errorMsg: "Invalid email"}
        }
      }
      return result
    },

    save () {
      let validate = this.validateModal()
      if(validate.result) {
        let data = this.createForm()
        if (this.editedIndex > -1) {
          data.append("id", this.editedItem.id)
          data.append("is_superuser", this.editedItem.type === "Admin")
          axios.post('http://localhost:8000/pitbull/user/edit/', data)
            .then(() => {
              this.$emit("editEmployee", this.editedItem)
              this.$notify({
                group: 'notifications-bottom-left',
                title: 'Success',
                text: 'Employee edited',
                type: 'success text-white'
              })
              this.close()
            })
            .catch(() => {
              this.$notify({
                group: 'notifications-bottom-left',
                title: 'Error',
                text: 'Employee edit error',
                type: 'error text-white'
              })
              this.close()
            })
        } else {
          if (this.editedItem.type === "Admin") {
            axios.post('http://localhost:8000/pitbull/superuser/create/', data)
              .then((response) => {
                this.editedItem['id'] = response.data.new_user_id
                this.addEmployee()
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Success',
                  text: 'Employee added',
                  type: 'success text-white'
                })
                this.close()
              })
              .catch((error) => {
                console.log(error)
                if (error.response.status === 409) {
                  this.$notify({
                    group: 'notifications-bottom-left',
                    title: 'Error',
                    text: error.response.data,
                    type: 'error text-white'
                  })
                } else {
                  this.$notify({
                    group: 'notifications-bottom-left',
                    title: 'Error',
                    text: 'Employee addition error',
                    type: 'error text-white'
                  })
                  this.close()
                }
              })
          } else {
            axios.post('http://localhost:8000/pitbull/user/create/', data)
              .then((response) => {
                this.editedItem['id'] = response.data.new_user_id
                this.addEmployee()
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Success',
                  text: 'Employee added',
                  type: 'success text-white'
                })
                this.close()
              })
              .catch((error) => {
                console.log(error.response.status)
                if (error.response.status === 409) {
                  this.$notify({
                    group: 'notifications-bottom-left',
                    title: 'Error',
                    text: error.response.data,
                    type: 'error text-white'
                  })
                } else {
                  this.$notify({
                    group: 'notifications-bottom-left',
                    title: 'Error',
                    text: 'Employee addition error',
                    type: 'error text-white'
                  })
                  this.close()
                }
              })
          }
        }
      }
      else {
        this.$notify({
          group: 'notifications-bottom-left',
          title: 'Error',
          text: validate.errorMsg,
          type: 'error text-white'
        })
      }
    },

    close() {
      this.$emit('closeModal')
    },

    addEmployee() {
      this.$emit("addEmployee", this.editedItem)
    },
  },
}
</script>

<style scoped>

</style>
