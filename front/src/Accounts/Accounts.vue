<template>
<div>
  <v-data-table
    style="width: 70%"
    :headers="headers"
    :items="employees"
    class="elevation-1 mx-auto mt-16 adminTable"
    loading-text="Loading... Please wait"
    :hide-default-footer="true"
    :loading="loading"
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
          @click:outside="close"
          :key="dialogKey"
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
          <employee-modal
            :formTitle="formTitle"
            :editedItem="editedItem"
            :editedIndex="editedIndex"
            @closeModal="close"
            @addEmployee="addEmployee"
            @editEmployee="editEmployee" />
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
import DialogDelete from "../components/DialogDelete"
import EmployeeModal from "../components/EmployeeModal"
import VueCookies from 'vue-cookies'
Vue.use(Vuetify)
Vue.use(VueCookies)

export default {
  name: "Accounts",
  data() {
    return {
      dialog: false,
      dialogKey: 0,
      search: '',
      page: 1,
      totalPages: 0,
      pageSize: 8,
      dialogDelete: false,
      adminTable: false,
      tableKey: 0,
      loading: true,
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
          text: 'Name',
          value: 'first_name',
          sortable: false,
          width: '30%'
        },
        {
          text: 'Surname',
          value: 'last_name',
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
      employees: [],
      editedIndex: -1,
      editedItem: {
        first_name: '',
        last_name: '',
        email: '',
        username: '',
        type: '',
        confirmPassword: '',
        password: '',
      },
      defaultItem: {
        first_name: '',
        last_name: '',
        email: '',
        username: '',
        type: '',
        confirmPassword: '',
        password: '',
      },
      deleteId: null,

    }
  },
  components: {
    DialogDelete,
    EmployeeModal
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
      this.getEmployees()
    },

    addEmployee (item) {
      this.getEmployees()
    },

    editEmployee (item) {
      this.getEmployees()
    },

    close () {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
        this.checkbox = false
        this.dialogKey += 1
      })
    },

    closeDelete () {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
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
      this.loading = true
      const params = this.getRequestParams(
        this.search,
        this.page,
        this.pageSize
      )

      axios.get('/pitbull/users/', {params: params})
        .then(response => {
          this.employees = response.data.users
          this.totalPages = response.data.totalPages
          this.page = parseInt(response.data.page)
          this.adminTable = true
          this.loading = false
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
