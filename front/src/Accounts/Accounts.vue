<template>
<div>
  <v-data-table
    style="width: 70%"
    :headers="headers"
    :items="employees"
    class="elevation-1 mx-auto mt-16"
    loading-text="Loading... Please wait"
    :hide-default-footer="true"
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
          @click:append="searchEmployees"
          @keyup.enter="searchEmployees"
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
        </v-dialog>
        <dialog-delete
          :dialogDelete="dialogDelete"
          :deleteId="deleteId"
          :editedIndex="editedIndex"
          :username="editedItem.username"
          @deleteFromArray="deleteFromArray"
          @closeDelete="closeDelete" />
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
  <v-pagination
    class="pagination"
    v-model="page"
    :length="totalPages"
    @input="pageChange"
    circle
    total-visible="7"
    next-icon="mdi-menu-right"
    prev-icon="mdi-menu-left"
  ></v-pagination>
</div>
</template>

<script>
import axios from "axios"
import Vue from 'vue'
import Vuetify from 'vuetify'
import dialogDelete from "../components/dialogDelete"
Vue.use(Vuetify)

export default {
  name: "Accounts",
  data: function () {
    return {
      dialog: false,
      search: '',
      page: 1,
      totalPages: 0,
      pageSize: 8,
      dialogDelete: false,
      adminTable: false,
      tableKey: 0,
      checkbox: false,
      headers: [
        {
          text: 'Username',
          align: 'start',
          value: 'username',
          sortable: false,
          width: '30%'
        },
        {
          text: 'Email',
          align: 'start',
          value: 'email',
          sortable: false,
          width: '30%'
        },
        {
          text: 'Employee',
          value: 'employee',
          sortable: false,
          width: '30%'
        },
        {
          text: 'Actions',
          value: 'actions',
          align: 'end',
          sortable: false,
          width: '10%'
        },
      ],
      type: ['Normal', 'Admin'],
      employees: [],
      editedIndex: -1,
      editedItem: {
        employee: '',
        email: '',
        username: '',
        type: '',
        confirmPassword: '',
        password: '',
      },
      defaultItem: {
        employee: '',
        email: '',
        username: '',
        type: '',
        confirmPassword: '',
        password: '',
      },
      deleteId: null,
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
  components: {
    dialogDelete
  },
  mounted() {
    let access = this.$cookies.get('access')
    let refresh = this.$cookies.get('refresh')
    if(access || refresh){
      this.getEmployees()
    }
    else {
      this.$router.push('/login')
    }
  },
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Employee' : 'Edit Employee'
    },
    isEdited () {
      return this.editedIndex !== -1
    },
    showPasswordModal () {
      return (!this.isEdited || this.checkbox)
    }
  },
  watch: {
    dialog (val) {
      val || this.close()
    },
    dialogDelete (val) {
      val || this.closeDelete()
    },
    checkbox () {
      this.editedItem.password = ''
      this.editedItem.confirmPassword = ''
    }
  },
  methods: {
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

    deleteFromArray (item) {
      this.employees.splice(item, 1)
    },

    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
        this.checkbox = false
      })
    },

    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

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
              Object.assign(this.employees[this.editedIndex], this.editedItem)
              this.$notify({
                group: 'notifications-bottom-left',
                title: 'Success',
                text: 'Employee edited',
                type: 'success text-white'
              })
              this.close()
            })
            .catch(errors => {
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
                this.employees.push(this.editedItem)
                this.employees.slice(-1)[0]['id'] = response.data.new_superuser_id
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Success',
                  text: 'Employee added',
                  type: 'success text-white'
                })
                this.close()
              })
              .catch(errors => {
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Error',
                  text: 'Employee addition error',
                  type: 'error text-white'
                })
                this.close()
              })
          } else {
            axios.post('http://localhost:8000/pitbull/user/create/', data)
              .then((response) => {
                this.employees.push(this.editedItem)
                this.employees.slice(-1)[0]['id'] = response.data.new_user_id
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Success',
                  text: 'Employee added',
                  type: 'success text-white'
                })
                this.close()
              })
              .catch(errors => {
                this.$notify({
                  group: 'notifications-bottom-left',
                  title: 'Error',
                  text: 'Employee addition error',
                  type: 'error text-white'
                })
                this.close()
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

    pageChange(value) {
      this.page = value
      this.getEmployees()
    },

    getRequestParams(search, page, pageSize) {
      let params = {}
      if (search) params["search"] = search
      if (page) params["page"] = page
      if (pageSize) params["size"] = pageSize

      return params
    },

    getEmployees() {
      const params = this.getRequestParams(
        this.search,
        this.page,
        this.pageSize
      )

      axios.get('http://localhost:8000/pitbull/users/', {params: params})
        .then(response => {
          this.employees = response.data.users
          this.totalPages = response.data.totalPages
          this.page = response.data.page
          this.adminTable = true
          this.tableKey += 1
        })
        .catch(() => {
          this.$router.push('/')
        })
    },

    searchEmployees() {
      this.page = 1
      this.getEmployees()
    }
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
.pagination {
  position: absolute;
  width: 100%;
  text-align: center;
  bottom: 0px;
}
</style>
