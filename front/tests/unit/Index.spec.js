import { mount, createLocalVue } from "@vue/test-utils"
import Index from '@/Products/Index'
import FeatureFilter from '@/Products/components/FeatureFilter'
import Vuetify from 'vuetify'
import VueRouter from "vue-router"
import Cookies from 'js-cookie';

export function main(cookieName) {
   const fullObjectStr = Cookies.get(cookieName);
   console.log(fullObjectStr);
}

describe('Index.vue', () => {
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
      wrapper = mount(Index, {
        localVue,
        vuetify,
        router,
        attachTo: '#root'
      })
      wrapper2 = mount(FeatureFilter, {
        localVue,
        vuetify,
        router
      })
    })
    
  afterEach(() => {
    wrapper.destroy()
  })
  it('Is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy()
  })
  it('Checks if user initially sees stockTable',  async () => {
    expect(wrapper.find('.stockTable').exists()).toBe(true)
  })
  it('Checks if user sees stockTable records',  async () => {
    const products = [
      {
        id: 1,
        symbol: "A_GAZ_ZIEMNY",
        name: "Gaz ziemny",
        group: 1,
        inventory: 0,
        features: 8,
        predictions: 4,
        is_archived: false
      },
      {
        id: 2,
        symbol: "A_OLEJ",
        name: "Olej napędowy",
        group: 1,
        inventory: 16,
        features: 8,
        predictions: 4,
        is_archived: false
      }
    ]
    await wrapper.setData({products: products})
    await wrapper.setData({stockTable: true})
    expect(wrapper.findAll('tbody tr').length).toBe(products.length)
  })

  it('Checks search function',  async () => {
   
    await wrapper.find('[data-test="search_product"]').trigger('focus')
    await wrapper.find('[data-test="search_product"]').setValue('gaz')
    expect(wrapper.findAll('tbody tr').length).toBe(1)
  })

  it('Checks search feature',  async () => {
    
    const group=[{
      id:1,
      name: "Podstawowa"
    }]
    await wrapper.setData({group: group})
    await wrapper.find('[data-test="group_feature"]').setValue('gaz')
    //await wrapper.find('[data-test="group_feature"]').setChecked()
  })
})
  