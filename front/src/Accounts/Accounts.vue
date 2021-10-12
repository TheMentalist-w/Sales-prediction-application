<template>
  <v-data-table
    style="width: 70%"
    :headers="headers"
    :items="employees"
    :search="search"
    class="elevation-1 mx-auto mt-16"
    loading-text="Loading... Please wait"
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
                      :rules="[rules.password]"
                      label="Confirm password"
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
import axios from "axios";

export default {
  name: "Accounts",
  data() {
    return {
      dialog: false,
      search: "",
      dialogDelete: false,
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
      employees: [
        {
          employee: 'Weronika M**k',
          email: 'weronikamk@02.pl',
          password: 'asd',
          type: 'Admin',
        },
        {
          employee: 'Weronika R**i',
          email: 'weronikari@02.pl',
          password: 'asd1',
          type: 'Normal',
        },
        {
          employee: 'Szymon S**a',
          email: 'szymonsa@02.pl',
          password: 'asd',
          type: 'Admin',
        },
        {
          employee: 'Jakub G**i',
          email: 'jakubgi@02.pl',
          password: 'asd',
          type: 'Normal',
        },
      ],
      editedIndex: -1,
      editedItem: {
        employee: '',
        email: '',
        password: '',
        confirmPassword: '',
        type: '',
      },
      defaultItem: {
        employee: '',
        email: '',
        password: '',
        type: '',
      },
      rules: {
        password: value => {
          return this.editedItem.password === this.editedItem.confirmPassword
        }
      },
    }
  },
  mounted() {
    axios.get('http://localhost:8000/pitbull/users/').then(data => console.log(data))
    let data = new FormData(); // 2

    data.append("username", '123')
    data.append("password", '123')

    axios.post('http://localhost:8000/pitbull/login/', data) // 4
     .then(res => alert("Form Submitted")) // 5
     .catch(errors => console.log(errors)) // 6
  },
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
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
    editItem (item) {
      this.editedIndex = this.employees.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.editedItem.confirmPassword = item.password
      this.dialog = true
    },

    deleteItem (item) {
      this.editedIndex = this.employees.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    deleteItemConfirm () {
      this.employees.splice(this.editedIndex, 1)
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
        Object.assign(this.employees[this.editedIndex], this.editedItem)
      } else {
        this.employees.push(this.editedItem)
      }
      this.close()
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
