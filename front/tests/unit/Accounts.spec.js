import { mount, createLocalVue } from "@vue/test-utils"
import Accounts from '@/Accounts/Accounts'
import Vuetify from 'vuetify'
import VueRouter from "vue-router"

describe('Accounts.vue', () => {
  let vuetify
  const localVue = createLocalVue()
  localVue.use(VueRouter)
  let wrapper
  let router
  beforeEach(() => {
    const div = document.createElement('div')
    div.id = 'root'
    document.body.appendChild(div)
    vuetify = new Vuetify()
    router = new VueRouter()
    wrapper = mount(Accounts, {
      localVue,
      vuetify,
      router,
      attachTo: '#root'
    })
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('Is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy()
  })

  it('Checks if user initially sees adminTable',  () => {
    expect(wrapper.find('.adminTable').exists()).toBe(false)
  })

  it('Checks if (admin) user sees adminTable',  async () => {
    await wrapper.setData({adminTable: true})
    await wrapper.setData({tableKey: 1})
    expect(wrapper.find('.adminTable').exists()).toBeTruthy()
  })

  it('Checks if (admin) user sees adminTable records',  async () => {
    const employees = [
      {
        id: 1,
        username: "test1",
        full_name: "test test",
        email: "test@test.test",
        type: "Normal"
      },
      {
        id: 2,
        username: "test2",
        full_name: "test2 test2",
        email: "test2@test.test",
        type: "Admin"
      }
    ]
    await wrapper.setData({employees: employees})
    await wrapper.setData({adminTable: true})
    await wrapper.setData({tableKey: 1})
    expect(wrapper.findAll('tbody tr').length).toBe(employees.length)
  })

  it('Checks if user cant see modals',  async () => {
    expect(wrapper.find('.v-dialog--active').exists()).toBeFalsy()
  })
})
