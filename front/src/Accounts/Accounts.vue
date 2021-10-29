<template>
  <v-data-table
    style="width: 70%"
    :headers="headers"
    :items="employees"
    :search="search"
    class="elevation-1 mx-auto mt-16"
    loading-text="Loading... Please wait"
    :key="tableKey"
    v-if="adminTable"
  >
    <template v-slot:top>
      <v-toolbar
        flat
      >
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-dialog
          v-model="dialog"
          max-width="500px"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              dark
              rounded
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-plus</v-icon>
              New
            </v-btn>
          </template>
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
                    ></v-text-field>
                  </v-col>
                  <v-col
                    cols="12"
                    md="6"
                  >
                    <v-text-field
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
                      v-model="editedItem.confirmPassword"
                      type="password"
                      :rules="[rules.password, rules.newUser]"
                      label="Confirm password"
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
        </v-dialog>
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
      </v-toolbar>
    </template>
    <template v-slot:item.actions="{ item }">
      <v-icon
        class="mr-2"
        color="secondary"
        @click="editItem(item)"
      >
        mdi-pencil
      </v-icon>
      <v-icon
        color="secondary"
        @click="deleteItem(item)"
      >
        mdi-delete
      </v-icon>
    </template>
  </v-data-table>
</template>

<script>
import axios from "axios"
import Vue from 'vue'
import Vuetify from 'vuetify'
Vue.use(Vuetify)

export default {
  name: "Accounts",
  data() {
    return {
      dialog: false,
      search: "",
      dialogDelete: false,
      adminTable: false,
      tableKey: 0,
      headers: [
        {
          text: 'Username',
          align: 'start',
          value: 'username',
          width: '30%'
        },
        {
          text: 'Email',
          align: 'start',
          value: 'email',
          width: '30%'
        },
        { text: 'Employee', value: 'employee', width: '30%' },
        { text: 'Actions', value: 'actions', sortable: false, align: 'end',  width: '10%' },
      ],
      type: ['Normal', 'Admin'],
      employees: [],
      editedIndex: -1,
      editedItem: {
        employee: '',
        email: '',
        username: '',
        type: '',
        password: '',
        confirmPassword: ''
      },
      defaultItem: {
        employee: '',
        email: '',
        username: '',
        type: '',
        password: '',
        confirmPassword: ''
      },
      deleteId: null,
      rules: {
        password: value => {
          let result = this.editedItem.password === this.editedItem.confirmPassword
          return result || "Password and ConfirmPassword don't match"
        },
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Invalid e-mail'
        },
        newUser: value => {
          return ((this.editedIndex < 0 && (value === null || value === '')) || this.checkbox) ? false : true
        }
      },
    }
  },
  mounted() {
    let logged = this.$cookies.get('access')
    if(logged) {
      axios.get('http://localhost:8000/pitbull/users/')
        .then(data => {
          this.employees = data.data.users
          this.adminTable = true
          this.tableKey += 1
        })
        .catch(() => {
          this.$router.push('/')
        })
    }
    else {
      this.$router.push('/login')
    }
  },
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Employee' : 'Edit Employee'
    },
  },
  watch: {
    dialog (val) {
      val || this.close()
    },
    dialogDelete (val) {
      val || this.closeDelete()
    },
  },
  methods: {
    clicks(){
      console.log(this.items)
    },
    editItem (item) {
      this.editedIndex = this.employees.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem (item) {
      this.editedIndex = this.employees.indexOf(item)
      this.deleteId = item.id
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm () {
      let user = this.editedItem
      axios.get('http://localhost:8000/pitbull/user/current/')
        .then((response) => {
          if(response.data === user.username) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Cannot delete yourself',
              type: 'error text-white'
            })
          } else {
            axios.delete('http://localhost:8000/pitbull/user/delete/'+this.deleteId.toString())
              .then(() => {
                this.employees.splice(this.editedIndex, 1)
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Success',
                  text: 'User deleted',
                  type: 'success text-white'
                })
              })
              .catch(errors => this.$notify({
                group: 'notifications-bottom-left',
                title: 'Error',
                text: 'Error deleting user',
                type: 'error text-white'
              }))
          }
        })
      this.closeDelete()
    },

    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    save () {
      if (this.editedIndex > -1) {
        let data = new FormData()
        data.append("id", this.editedItem.email)
        data.append("fist_name", this.editedItem.employee.split(' ')[0])
        data.append("last_name", this.editedItem.employee.split(' ')[1])
        data.append("email",this.editedItem.email)
        data.append("username",this.editedItem.username)
        data.append("password", this.editedItem.password)
        data.append("confirmPassword", this.editedItem.confirmPassword)
        data.append("type", (this.editedItem.type==="Admin").toString())
        axios.post('http://localhost:8000/pitbull/user/edit/', data)
        .then(() => {
          Object.assign(this.employees[this.editedIndex], this.editedItem)
          this.close()
        })
        .catch(errors => {
          this.$notify({
            group: 'notifications-bottom-left',
            title: 'Error',
            text: 'User update error',
            type: 'error text-white'
          })
          this.close()
        })
      } else {
        let data = new FormData()
        data.append("id", this.editedItem.email)
        data.append("fist_name", this.editedItem.employee.split(' ')[0])
        data.append("last_name", this.editedItem.employee.split(' ')[1])
        data.append("email",this.editedItem.email)
        data.append("username",this.editedItem.username)
        data.append("password", this.editedItem.password)
        data.append("confirmPassword", this.editedItem.confirmPassword)
        data.append("type", (this.editedItem.type==="Admin").toString())
        axios.post('http://localhost:8000/pitbull/user/create/', data)
        .then((response) => {
          this.employees.push(this.editedItem)
          this.close()
          this.employees.slice(-1)[0]['id'] = response.data.id
        })
        .catch(errors => {
          this.$notify({
            group: 'notifications-bottom-left',
            title: 'Error',
            text: 'Błąd dodawania użytkownika',
            type: 'error text-white'
          })
          this.close()
        }) // 6
      }
    },
  },
}
</script>

<style>
.v-data-table th {
  font-size: 28px !important;
}
.v-data-table td {
  font-size: 20px !important;
}
</style>
