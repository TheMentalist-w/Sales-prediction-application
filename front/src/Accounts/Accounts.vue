<template>
  <div style="display: flex; flex-direction: column; height: 100%">
    <v-container
      fluid
      style="height: 100%"
    >
      <v-layout column>
        <v-flex>
          <v-data-table
            v-if="adminTable"
            :key="tableKey"
            style="width: 70%"
            :headers="headers"
            :items="employees"
            class="elevation-1 mx-auto mt-16 adminTable"
            loading-text="Loading... Please wait"
            :hide-default-footer="true"
            :loading="loading"
          >
            <template v-slot:top>
              <v-toolbar
                flat
              >
                <v-text-field
                  v-model="search"
                  style="padding-right: 20px"
                  append-icon="mdi-magnify"
                  single-line
                  label="Search"
                  hide-details
                  @click:append="searchEmployees"
                  @keyup.enter="searchEmployees"
                />

                <v-dialog
                  :key="dialogKey"
                  v-model="dialog"
                  max-width="500px"
                  @click:outside="close"
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
                    :form-title="formTitle"
                    :edited-item="editedItem"
                    :edited-index="editedIndex"
                    @closeModal="close"
                    @addEmployee="addEmployee"
                    @editEmployee="editEmployee"
                  />
                </v-dialog>
                <dialog-delete
                  :dialog-delete="dialogDelete"
                  :delete-id="deleteId"
                  :edited-index="editedIndex"
                  :username="editedItem.username"
                  @deleteFromArray="deleteFromArray"
                  @closeDelete="closeDelete"
                />
                <v-spacer />
                <v-spacer />
                <v-spacer />
                <v-select
                  v-model="pageSize"
                  style="margin-top: 25px; width: 1%"
                  :items="pageSizes"
                  label="Items on page"
                  @change="changePageSize"
                />
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
        </v-flex>
      </v-layout>
    </v-container>
    <v-pagination
      v-model="page"
      style="align-items: flex-end"
      :length="totalPages"
      circle
      total-visible="7"
      next-icon="mdi-menu-right"
      prev-icon="mdi-menu-left"
      @input="pageChange"
    />
  </div>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';
import Vuetify from 'vuetify';
import DialogDelete from '../components/DialogDelete';
import EmployeeModal from '../components/EmployeeModal';
import VueCookies from 'vue-cookies';

Vue.use(Vuetify);
Vue.use(VueCookies);

export default {
  name: 'Accounts',
  components: {
    DialogDelete,
    EmployeeModal
  },
  data () {
    return {
      dialog: false,
      dialogKey: 0,
      search: '',
      page: 1,
      totalPages: 0,
      pageSize: 25,
      pageSizes: [10, 25, 50, 100],
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
          width: '22%'
        },
        {
          text: 'Email',
          align: 'start',
          value: 'email',
          sortable: false,
          width: '25%'
        },
        {
          text: 'Name',
          value: 'first_name',
          sortable: false,
          width: '22%'
        },
        {
          text: 'Surname',
          value: 'last_name',
          sortable: false,
          width: '22%'
        },
        {
          text: 'Actions',
          value: 'actions',
          align: 'end',
          sortable: false,
          width: '10%'
        }
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
        password: ''
      },
      defaultItem: {
        first_name: '',
        last_name: '',
        email: '',
        username: '',
        type: '',
        confirmPassword: '',
        password: ''
      },
      deleteId: null
    };
  },
  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Employee' : 'Edit Employee';
    }
  },
  watch: {
    dialog (val) {
      val || this.close();
    },
    dialogDelete (val) {
      val || this.closeDelete();
    },
    checkbox () {
      this.editedItem.password = '';
      this.editedItem.confirmPassword = '';
    }
  },
  mounted () {
    const access = this.$cookies.get('access');
    const refresh = this.$cookies.get('refresh');
    if (access || refresh) {
      this.getEmployees();
    } else {
      this.$router.push('/login');
    }
  },
  methods: {
    editItem (item) {
      this.editedIndex = this.employees.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem (item) {
      this.editedIndex = this.employees.indexOf(item);
      this.deleteId = item.id;
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteFromArray () {
      this.getEmployees();
    },

    addEmployee () {
      this.getEmployees();
    },

    editEmployee () {
      this.getEmployees();
    },

    close () {
      this.dialog = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
        this.checkbox = false;
        this.dialogKey += 1;
      });
    },

    closeDelete () {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    pageChange (value) {
      this.page = value;
      this.getEmployees();
    },

    getRequestParams (search, page, pageSize) {
      const params = {};
      if (search) params.search = search;
      if (page) params.page = page;
      if (pageSize) params.size = pageSize;

      return params;
    },

    getEmployees () {
      this.loading = true;
      const params = this.getRequestParams(
        this.search,
        this.page,
        this.pageSize
      );

      axios.get('/user_auth/', { params: params })
        .then(response => {
          this.employees = response.data.users;
          this.totalPages = response.data.totalPages;
          this.page = parseInt(response.data.page);
          this.adminTable = true;
          this.loading = false;
          this.tableKey += 1;
        })
        .catch(error => {
          if (error.response.status === 500) {
            this.$notify({
              group: 'notifications-bottom-left',
              title: 'Error',
              text: 'Server error. Try later',
              type: 'error text-white'
            });
          } else {
            this.$router.push('/');
          }
        });
    },

    searchEmployees () {
      this.page = 1;
      this.getEmployees();
    },

    changePageSize () {
      this.getEmployees();
    }
  }
};
</script>

<style>
</style>
