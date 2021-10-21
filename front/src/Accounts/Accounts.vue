<template>
  <v-data-table
    style="width: 70%"
    :headers="headers"
    :items="employees"
    :search="search"
    class="elevation-1 mx-auto mt-16"
    loading-text="Loading... Please wait"
    :key="tableKey"
    v-if="loggedIn"
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
      loggedIn: false,
      tableKey: 0,
      headers: [
        {
          text: 'Email',
          align: 'start',
          value: 'email',
          width: '45%',
        },
        { text: 'Employee', value: 'employee', width: '45%', },
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
      },
      defaultItem: {
        employee: '',
        email: '',
        username: '',
        type: '',
      },
      deleteId: null,
      rules: {
        password: value => {
          return this.editedItem.password === this.editedItem.confirmPassword
        },
        newUser: () => {
          return this.editedIndex < 0 ? false : true
        }
      },
    }
  },
  beforeMount() {
    this.$vuetify.theme.dark = sessionStorage.getItem('pit_theme') === "true" ? true : false
  },
  mounted() {
    let logged = this.$cookies.get('authToken')
    if(logged){
      this.loggedIn = true
      this.tableKey += 1
    }
    else {
      this.$router.push(this.$route.query.redirect || '/login')
    }
    
    const config = {
      headers: { Authorization: `Token ${this.$cookies.get('authToken')}` }
    }
    axios.get('http://localhost:8000/pitbull/users/', config).then(data => {
      this.employees = data.data.users
      this.tableKey += 1
    })
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
      let data = new FormData()
      data.append("id", this.deleteId)
      data.append("token", )
      axios.post('http://localhost:8000/pitbull/user/delete/', data)
      .then(() => this.employees.splice(this.editedIndex, 1))
      .catch(errors => this.$notify({group: 'notifications-bottom-left', title: 'Error', text:'Błąd usuwania użytkownika', type: 'error text-white' })) // 6
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
        data.append("type", this.editedItem.type==="Admin" ? true : false)
        axios.post('http://localhost:8000/pitbull/user/edit/', data)
        .then(() => {
          Object.assign(this.employees[this.editedIndex], this.editedItem)
          this.close()
        })
        .catch(errors => {
          this.$notify({group: 'notifications-bottom-left', title: 'Error', text:'Błąd edycji użytkownika', type: 'error text-white' })
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
        data.append("type", this.editedItem.type==="Admin" ? true : false)
        axios.post('http://localhost:8000/pitbull/user/create/', data)
        .then((response) => {
          this.employees.push(this.editedItem)
          this.close()
          this.employees.slice(-1)[0]['id'] = response.data.id
        })
        .catch(errors => {
          this.$notify({group: 'notifications-bottom-left', title: 'Error', text:'Błąd dodawania użytkownika', type: 'error text-white' })
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
