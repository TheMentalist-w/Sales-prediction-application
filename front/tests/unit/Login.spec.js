import { mount, createLocalVue } from "@vue/test-utils"
import Login from '@/Auth/Login'
import Vuetify from 'vuetify'

describe('Login.vue', () => {
  let vuetify
  const localVue = createLocalVue()
  beforeEach(()=>{
    vuetify = new Vuetify()
  })

  it('Is a Vue instance', () => {
    const wrapper = mount(Login, {
      localVue,
      vuetify,
    })
    expect(wrapper.isVueInstance).toBeTruthy()
    wrapper.destroy()
  })


  it('Checks if user initially sees loginBox',  () => {
    const wrapper = mount(Login, {
      localVue,
      vuetify,
    })
    expect(wrapper.find('.loginBox').exists()).toBe(false)
    wrapper.destroy()
  })

  it('Checks if user without cookies sees username field', async () => {
    const wrapper = mount(Login, {
      localVue,
      vuetify,
    })

    await wrapper.setData({loginBox: true})
    await wrapper.setData({loggedKey: 1})

    expect(wrapper.find('[data-test="username"]').exists()).toBe(true)
    wrapper.destroy()
  })

  it('Checks if user without cookies sees password field', async () => {
    const wrapper = mount(Login, {
      localVue,
      vuetify,
    })

    await wrapper.setData({loginBox: true})
    await wrapper.setData({loggedKey: 1})

    expect(wrapper.find('[data-test="password"]').exists()).toBe(true)
    wrapper.destroy()
  })

  it('Checks if user see required validation for username field', async () => {
    const div = document.createElement('div')
    div.id = 'root'
    document.body.appendChild(div)
    const wrapper = mount(Login, {
      localVue,
      vuetify,
      attachTo: '#root'
    })
    
    await wrapper.setData({loginBox: true})
    await wrapper.setData({loggedKey: 1})
    await wrapper.find('[data-test="username"]').trigger('focus')
    await wrapper.find('[data-test="password"]').trigger('focus')
    
    expect(wrapper.find('.username .v-text-field__details').text()).toContain('Required.')
    wrapper.destroy()
  })

  it('Checks if user see required validation for password field', async () => {
    const div = document.createElement('div')
    div.id = 'root'
    document.body.appendChild(div)
    const wrapper = mount(Login, {
      localVue,
      vuetify,
      attachTo: '#root'
    })
    
    await wrapper.setData({loginBox: true})
    await wrapper.setData({loggedKey: 1})
    await wrapper.find('[data-test="password"]').trigger('focus')
    await wrapper.find('[data-test="username"]').trigger('focus')
    
    expect(wrapper.find('.password .v-text-field__details').text()).toContain('Required.')
    wrapper.destroy()
  })
})
