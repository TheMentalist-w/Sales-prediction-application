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

})
