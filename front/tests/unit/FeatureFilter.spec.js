import { mount, createLocalVue } from '@vue/test-utils';
import FeatureFilter from '@/Products/components/FeatureFilter';
import Vuetify from 'vuetify';
// import VueRouter from "vue-router"

describe('FeatureFilter.vue', () => {
  let vuetify;
  const localVue = createLocalVue();
  // localVue.use(VueRouter)
  let wrapper;
  // let router
  beforeEach(() => {
    const div = document.createElement('div');
    div.id = 'root';
    document.body.appendChild(div);
    vuetify = new Vuetify();
    // router = new VueRouter()
    wrapper = mount(FeatureFilter, {
      localVue,
      vuetify,
      attachTo: '#root',
      propsData: { filters: [], filtered: [] }
    });
  });

  afterEach(() => {
    wrapper.destroy();
  });
  it('Is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy();
  });
});
