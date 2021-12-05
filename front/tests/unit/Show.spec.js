import { mount, createLocalVue } from "@vue/test-utils"
import Show from '@/Products/Show'
import Vuetify from 'vuetify'
import VueRouter from "vue-router"

describe('Show.vue', () => {
    let vuetify
    const localVue = createLocalVue()
    let wrapper
    let router
    beforeEach(() => {
      const div = document.createElement('div')
      div.id = 'root'
      document.body.appendChild(div)
      vuetify = new Vuetify()
      router = new VueRouter()
      wrapper = mount(Show, {
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
  